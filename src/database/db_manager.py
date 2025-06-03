import os
import sqlite3
import uuid
import re
from datetime import datetime

class DBManager:
    """数据库管理类，负责管理聊天历史和会话记录"""
    
    def __init__(self, db_path="chat_history.db"):
        """
        初始化数据库管理器
        
        Args:
            db_path: 数据库文件路径
        """
        self.db_path = db_path
        self._init_database()
    
    def _connect(self):
        """
        连接到SQLite数据库
        
        Returns:
            sqlite3.Connection: 数据库连接对象
        """
        return sqlite3.connect(self.db_path)
    
    def _init_database(self):
        """初始化数据库结构"""
        conn = self._connect()
        cursor = conn.cursor()
        
        # 创建会话表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            client_id TEXT,
            session_file TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 创建聊天历史记录表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            session_file TEXT,
            client_id TEXT,
            question TEXT,
            answer TEXT,
            created_at TIMESTAMP,
            llm_type TEXT,
            model_name TEXT,
            has_chart BOOLEAN DEFAULT 0,
            chart_path TEXT,
            FOREIGN KEY (session_id) REFERENCES sessions(id)
        )
        ''')
        
        # 检查是否需要迁移旧数据
        cursor.execute("PRAGMA table_info(chat_history)")
        columns = [row[1] for row in cursor.fetchall()]
        
        # 如果缺少新增的列，进行迁移
        missing_columns = []
        if 'has_chart' not in columns:
            missing_columns.append('has_chart BOOLEAN DEFAULT 0')
        if 'chart_path' not in columns:
            missing_columns.append('chart_path TEXT')
        if 'llm_type' not in columns and 'model' not in columns:
            missing_columns.append('llm_type TEXT')
        if 'model_name' not in columns:
            missing_columns.append('model_name TEXT')
        if 'client_id' not in columns and 'question_id' in columns:
            # 重命名列，需要特殊处理
            print("需要从question_id迁移到client_id，将创建新表...")
            self._migrate_from_old_structure(conn, cursor)
        elif missing_columns:
            # 添加缺少的列
            for column_def in missing_columns:
                try:
                    cursor.execute(f"ALTER TABLE chat_history ADD COLUMN {column_def}")
                    print(f"数据库表已添加新列: {column_def}")
                except sqlite3.OperationalError as e:
                    print(f"添加列失败: {str(e)}")
        
        conn.commit()
        conn.close()
    
    def _migrate_from_old_structure(self, conn, cursor):
        """迁移旧的表结构到新的表结构"""
        try:
            # 创建一个临时表
            cursor.execute('''
            CREATE TABLE chat_history_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                session_file TEXT,
                client_id TEXT,
                question TEXT,
                answer TEXT,
                created_at TIMESTAMP,
                llm_type TEXT,
                model_name TEXT,
                has_chart BOOLEAN DEFAULT 0,
                chart_path TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            )
            ''')
            
            # 从旧表复制数据到新表
            cursor.execute('''
            INSERT INTO chat_history_new (
                session_id, session_file, client_id, question, answer, created_at, llm_type, model_name
            )
            SELECT 
                session_id, 
                session_file, 
                question_id as client_id, 
                question, 
                answer, 
                timestamp as created_at,
                model as llm_type,
                model_name
            FROM 
                chat_history
            ''')
            
            # 删除旧表
            cursor.execute("DROP TABLE chat_history")
            
            # 重命名新表
            cursor.execute("ALTER TABLE chat_history_new RENAME TO chat_history")
            
            conn.commit()
            print("数据库结构迁移成功")
        except Exception as e:
            conn.rollback()
            print(f"数据库迁移失败: {str(e)}")
    
    def save_chat_history(self, session_id, session_file, client_id, question, answer, llm_type, model_name=None, chart_path=None):
        """
        保存聊天历史记录
        
        Args:
            session_id: 会话ID
            session_file: 会话文件名
            client_id: 客户端ID
            question: 用户问题
            answer: AI回答
            llm_type: AI模型类型
            model_name: 具体模型名称
            chart_path: 图表文件路径（如果有）
        """
        try:
            # 如果直接传入了图表路径，使用它
            has_chart = bool(chart_path and os.path.exists(chart_path))
            final_chart_path = os.path.abspath(chart_path) if has_chart else None
            
            # 如果没有直接传入图表路径，尝试从回答文本中检测
            if not has_chart:
                # 检测是否包含图表路径
                has_img = False
                img_path = None
                
                # 提取图表路径 - 检查常见的格式
                # 1. 检查是否有图片URL链接
                if "图片URL链接:" in answer:
                    has_img = True
                    
                # 2. 检查是否有本地图片路径
                elif "本地图片路径:" in answer:
                    has_img = True
                    # 尝试提取图片路径
                    path_matches = re.findall(r'本地图片路径:\s+(.+?)(?:\n|$)', answer)
                    if path_matches:
                        original_path = path_matches[0].strip()
                        # 转换为绝对路径
                        img_path = os.path.abspath(original_path) if not os.path.isabs(original_path) else original_path
                
                # 3. 检查Markdown图片格式 ![Chart](file://...) 或 ![Chart](charts/...)
                elif re.search(r'!\[.*?\]\((file://)?(.+?\.(png|jpg|jpeg|svg))\)', answer):
                    has_img = True
                    # 提取Markdown图片路径
                    markdown_matches = re.findall(r'!\[.*?\]\((file://)?(.+?\.(png|jpg|jpeg|svg))\)', answer)
                    if markdown_matches:
                        # 获取第一个匹配的路径
                        file_protocol, path_part, ext = markdown_matches[0]
                        original_path = path_part.strip()
                        # 如果路径不是绝对路径，转换为绝对路径
                        img_path = os.path.abspath(original_path) if not os.path.isabs(original_path) else original_path
                
                # 4. 检查是否有图片文件路径行 (单独的路径行)
                elif re.search(r'charts/\d+_[a-zA-Z0-9]+\.(png|jpg|jpeg|svg)(?:\n|$)', answer):
                    has_img = True
                    path_matches = re.findall(r'(charts/\d+_[a-zA-Z0-9]+\.(png|jpg|jpeg|svg))(?:\n|$)', answer)
                    if path_matches:
                        original_path = path_matches[0][0].strip()
                        # 转换为绝对路径
                        img_path = os.path.abspath(original_path)
                
                # 5. 检查新格式：[数据分析图表: filename.png]
                elif re.search(r'\[.*?图表.*?:\s*(.+?\.(png|jpg|jpeg|svg))\]', answer):
                    has_img = True
                    # 提取图表文件名
                    chart_matches = re.findall(r'\[.*?图表.*?:\s*(.+?\.(png|jpg|jpeg|svg))\]', answer)
                    if chart_matches:
                        filename = chart_matches[0][0].strip()
                        # 在可能的目录中查找这个文件
                        possible_dirs = ["charts", "exports/charts", "."]
                        for dir_path in possible_dirs:
                            full_path = os.path.join(dir_path, filename)
                            if os.path.exists(full_path):
                                img_path = os.path.abspath(full_path)
                                break
                
                has_chart = has_img and img_path and os.path.exists(img_path)
                final_chart_path = img_path if has_chart else None
            
            conn = self._connect()
            cursor = conn.cursor()
            
            # 插入新记录
            cursor.execute(
                '''
                INSERT INTO chat_history (
                    session_id, session_file, client_id, question, answer, 
                    created_at, llm_type, model_name, has_chart, chart_path
                ) VALUES (?, ?, ?, ?, ?, datetime('now', 'localtime'), ?, ?, ?, ?)
                ''',
                (
                    session_id, session_file, client_id, question, answer, 
                    llm_type, model_name or llm_type, has_chart, final_chart_path
                )
            )
            
            conn.commit()
            conn.close()
            
            if has_chart:
                print(f"✅ 图表记录已保存: {final_chart_path}")
            
        except Exception as e:
            print(f"创建会话记录失败: {str(e)}")
    
    def get_sessions_for_client(self, client_id):
        """
        获取特定客户端的所有会话记录
        
        Args:
            client_id: 客户端ID
            
        Returns:
            list: 会话记录列表
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT session_id, session_file, timestamp FROM sessions WHERE client_id=? ORDER BY timestamp DESC",
            (client_id,)
        )
        sessions = cursor.fetchall()
        conn.close()
        
        return [{"session_id": s[0], "session_file": s[1], "timestamp": s[2]} for s in sessions]
    
    def get_all_sessions(self):
        """
        获取所有会话记录
        
        Returns:
            list: 所有会话记录列表
        """
        try:
            conn = self._connect()
            cursor = conn.cursor()
            
            cursor.execute(
                """
                SELECT 
                    id as session_id, 
                    session_file, 
                    created_at as timestamp 
                FROM 
                    sessions 
                ORDER BY 
                    created_at DESC
                """
            )
            
            sessions = cursor.fetchall()
            conn.close()
            
            result = []
            for s in sessions:
                result.append({
                    "session_id": s[0],
                    "session_file": s[1],
                    "timestamp": s[2]
                })
                
            return result
        except Exception as e:
            print(f"获取所有会话记录时出错: {str(e)}")
            return []
    
    def get_chat_history_for_session(self, session_id):
        """
        获取特定会话的聊天历史记录
        
        Args:
            session_id: 会话ID
        
        Returns:
            list: 聊天记录列表
        """
        if not session_id:
            return []
        
        conn = self._connect()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(
            '''
            SELECT 
                id, session_id, question, answer, created_at, llm_type, model_name, has_chart, chart_path
            FROM 
                chat_history 
            WHERE 
                session_id = ? 
            ORDER BY 
                created_at
            ''',
            (session_id,)
        )
        
        rows = cursor.fetchall()
        conn.close()
        
        result = []
        for row in rows:
            chat_entry = dict(row)
            
            # 如果有图表，确保路径在回答中
            if chat_entry.get('has_chart') and chat_entry.get('chart_path'):
                chart_path = chat_entry['chart_path']
                if os.path.exists(chart_path):
                    # 确保路径是绝对路径并使用正斜杠
                    absolute_path = os.path.abspath(chart_path).replace('\\', '/')
                    
                    # 处理回答中的图表路径
                    answer_text = chat_entry['answer']
                    
                    # 移除任何现有的图表路径文本行
                    if "本地图片路径:" in answer_text:
                        parts = answer_text.split("本地图片路径:")
                        answer_text = parts[0].strip()
                    
                    # 移除已有的图表路径
                    chart_patterns = [
                        r'charts/\d+_[a-zA-Z0-9]+\.(png|jpg|jpeg|svg)',
                        r'files/charts/\d+_[a-zA-Z0-9]+\.(png|jpg|jpeg|svg)',
                        r'[A-Za-z]:\\[^<>:|?*\n]+\.(png|jpg|jpeg|svg)',  # Windows绝对路径
                        r'/[^<>:|?*\n]+\.(png|jpg|jpeg|svg)'  # Unix绝对路径
                    ]
                    
                    for pattern in chart_patterns:
                        answer_text = re.sub(pattern, '', answer_text)
                    
                    # 清理多余的空行
                    answer_text = re.sub(r'\n{3,}', '\n\n', answer_text)
                    answer_text = answer_text.strip()
                    
                    # 添加图表绝对路径作为单独的行
                    if answer_text:
                        answer_text += "\n\n"
                    
                    # 直接添加图片绝对路径，这将被Gradio识别为图片
                    answer_text += absolute_path
                    
                    # 添加一个额外的图片绝对路径说明
                    answer_text += f"\n\n本地图片路径: {absolute_path}"
                    
                    # 更新回答文本
                    chat_entry['answer'] = answer_text
            
            result.append(chat_entry)
        
        return result
    
    def create_session(self, client_id, file_name):
        """
        创建新会话
        
        Args:
            client_id: 客户端ID
            file_name: 数据文件名
            
        Returns:
            str: 新会话ID
        """
        session_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session_file = f"{file_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO sessions (session_id, session_file, timestamp, client_id) VALUES (?, ?, ?, ?)",
                (session_id, session_file, timestamp, client_id)
            )
            conn.commit()
        except Exception as e:
            print(f"创建会话记录失败: {str(e)}")
        finally:
            conn.close()
        
        return session_id, session_file
    
    def get_session_file_by_id(self, session_id):
        """
        根据会话ID获取会话文件名
        
        Args:
            session_id: 会话ID
            
        Returns:
            str: 会话文件名
        """
        # 如果session_id是字典，尝试提取值
        if isinstance(session_id, dict) and "value" in session_id:
            session_id = session_id["value"]
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT session_file FROM sessions WHERE session_id=?", (session_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0]
        return None
    
    def display_all_history(self):
        """
        获取所有聊天历史记录用于显示
        
        Returns:
            list: 包含所有聊天记录的列表，格式化为显示用的格式
        """
        conn = self._connect()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(
            '''
            SELECT 
                chat_history.id, 
                chat_history.session_id,
                chat_history.session_file, 
                chat_history.question, 
                chat_history.answer, 
                chat_history.created_at,
                chat_history.llm_type,
                chat_history.model_name,
                chat_history.has_chart,
                chat_history.chart_path
            FROM 
                chat_history 
            ORDER BY 
                chat_history.created_at DESC
            LIMIT 20
            '''
        )
        
        rows = cursor.fetchall()
        conn.close()
        
        result = []
        
        # 如果没有记录，返回空结果
        if not rows:
            return []
            
        for row in rows:
            # 格式化时间 - 只显示日期和时间，不显示秒
            created_at = row['created_at']
            if created_at and len(created_at) > 16:
                created_at = created_at[:16]
            
            # 限制问题的长度
            question = row['question']
            if len(question) > 50:
                question = question[:50] + "..."
                
            # 处理回答及图表
            answer = row['answer']
            answer_text = self._format_answer_for_display(answer, row)
                
            # 添加模型标记
            model_info = row['model_name'] if row['model_name'] else row['llm_type']
            model_info = model_info.replace("gpt-3.5-turbo", "GPT-3.5").replace("gpt-4", "GPT-4")
            
            # 添加会话ID和文件名，格式为：session_file (session_id)
            session_id = row['session_id']
            session_file = row['session_file']
            session_info = f"{session_file} ({session_id[:8]}...)"
            
            # 移除record_id列，只返回4列数据: 时间, 会话ID, 问题, 回答
            result.append([
                f"{created_at} ({model_info})",  # 时间与模型
                session_info,                    # 会话ID与文件名
                question,                        # 问题
                answer_text                      # 回答
            ])
        
        return result
    
    def _format_answer_for_display(self, answer, row):
        """格式化回答用于显示"""
        # 限制长度为120字符
        MAX_LENGTH = 120
        
        # 如果回答为空，返回空字符串
        if not answer:
            return ""
            
        # 处理回答文本
        answer_text = answer
        
        # 如果有图表，添加标记
        if row['has_chart'] and row['chart_path'] and os.path.exists(row['chart_path']):
            if len(answer_text) > MAX_LENGTH:
                answer_text = answer_text[:MAX_LENGTH] + "... [图表]"
            else:
                answer_text += " [图表]"
        elif len(answer_text) > MAX_LENGTH:
            answer_text = answer_text[:MAX_LENGTH] + "..."
            
        return answer_text
    
    def delete_session_history(self, session_id):
        """
        删除指定会话的所有聊天记录
        
        Args:
            session_id: 会话ID
            
        Returns:
            bool: 删除操作是否成功
        """
        if not session_id:
            return False
            
        # 如果session_id是字典，尝试提取值
        if isinstance(session_id, dict) and "value" in session_id:
            session_id = session_id["value"]
        
        try:
            conn = self._connect()
            cursor = conn.cursor()
            
            # 查询该会话的图表文件路径，以便删除文件
            cursor.execute(
                "SELECT chart_path FROM chat_history WHERE session_id = ? AND has_chart = 1",
                (session_id,)
            )
            chart_paths = cursor.fetchall()
            
            # 删除会话的所有聊天记录
            cursor.execute(
                "DELETE FROM chat_history WHERE session_id = ?",
                (session_id,)
            )
            
            conn.commit()
            conn.close()
            
            # 删除对应的图表文件
            for path_row in chart_paths:
                chart_path = path_row[0]
                if chart_path and os.path.exists(chart_path):
                    try:
                        os.remove(chart_path)
                    except Exception as e:
                        print(f"删除图表文件失败: {chart_path}, 错误: {str(e)}")
            
            return True
        except Exception as e:
            print(f"删除会话历史记录失败: {str(e)}")
            return False
    
    def delete_all_history(self):
        """
        删除所有聊天记录和会话记录
        
        Returns:
            bool: 删除操作是否成功
        """
        try:
            conn = self._connect()
            cursor = conn.cursor()
            
            # 查询所有图表文件路径，以便删除文件
            cursor.execute(
                "SELECT chart_path FROM chat_history WHERE has_chart = 1"
            )
            chart_paths = cursor.fetchall()
            
            # 删除所有聊天记录
            cursor.execute("DELETE FROM chat_history")
            
            # 可选：删除所有会话记录
            # cursor.execute("DELETE FROM sessions")
            
            conn.commit()
            conn.close()
            
            # 删除所有图表文件
            for path_row in chart_paths:
                chart_path = path_row[0]
                if chart_path and os.path.exists(chart_path):
                    try:
                        os.remove(chart_path)
                    except Exception as e:
                        print(f"删除图表文件失败: {chart_path}, 错误: {str(e)}")
            
            return True
        except Exception as e:
            print(f"删除所有历史记录失败: {str(e)}")
            return False
            
    def get_session_id_by_details(self, timestamp, question_prefix):
        """
        根据时间戳和问题前缀获取会话ID
        
        Args:
            timestamp: 时间戳，格式为"YYYY-MM-DD HH:MM"
            question_prefix: 问题的前缀（可能被截断）
            
        Returns:
            str: 会话ID或空字符串
        """
        try:
            conn = self._connect()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # 构建模糊查询
            time_pattern = f"{timestamp}%"
            question_pattern = f"{question_prefix}%"
            
            # 查询匹配的记录
            cursor.execute(
                '''
                SELECT 
                    session_id
                FROM 
                    chat_history 
                WHERE 
                    created_at LIKE ? AND
                    question LIKE ?
                ORDER BY 
                    created_at DESC
                LIMIT 1
                ''',
                (time_pattern, question_pattern)
            )
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return row['session_id']
            return ""
        except Exception as e:
            print(f"根据详情获取会话ID时出错: {str(e)}")
            return ""
    
    def delete_record(self, record_id):
        """
        删除单条聊天记录
        
        Args:
            record_id: 记录ID
            
        Returns:
            bool: 删除操作是否成功
        """
        if not record_id:
            return False
        
        try:
            conn = self._connect()
            cursor = conn.cursor()
            
            # 获取记录信息，查看是否有图表
            cursor.execute(
                "SELECT has_chart, chart_path FROM chat_history WHERE id = ?",
                (record_id,)
            )
            record = cursor.fetchone()
            
            # 删除记录
            cursor.execute("DELETE FROM chat_history WHERE id = ?", (record_id,))
            deleted = cursor.rowcount > 0
            
            conn.commit()
            conn.close()
            
            # 如果有图表，删除图表文件
            if record and record[0] and record[1] and os.path.exists(record[1]):
                try:
                    os.remove(record[1])
                except Exception as e:
                    print(f"删除图表文件失败: {record[1]}, 错误: {str(e)}")
            
            return deleted
        except Exception as e:
            print(f"删除记录失败: {str(e)}")
            return False
    
    def get_session_id_by_record_id(self, record_id):
        """
        通过记录ID获取会话ID
        
        Args:
            record_id: 记录ID
            
        Returns:
            str: 会话ID或空字符串
        """
        try:
            conn = self._connect()
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT session_id FROM chat_history WHERE id = ?",
                (record_id,)
            )
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return result[0]
            return ""
        except Exception as e:
            print(f"通过记录ID获取会话ID时出错: {str(e)}")
            return ""
    
    def get_record_by_time_and_question(self, time_question_info):
        """
        通过时间和问题信息获取记录ID
        
        Args:
            time_question_info: 格式为"时间信息|问题信息"的字符串
            
        Returns:
            str: 记录ID或空字符串
        """
        try:
            if not time_question_info or '|' not in time_question_info:
                return ""
                
            parts = time_question_info.split('|', 1)
            time_info = parts[0]
            question_info = parts[1]
            
            # 提取时间戳部分（去掉模型信息）
            if '(' in time_info:
                timestamp = time_info.split('(')[0].strip()
            else:
                timestamp = time_info.strip()
            
            # 如果问题以"..."结尾，说明被截断了，需要用模糊匹配
            if question_info.endswith("..."):
                question_prefix = question_info[:-3]  # 去掉"..."
                is_truncated = True
            else:
                question_prefix = question_info
                is_truncated = False
            
            conn = self._connect()
            cursor = conn.cursor()
            
            if is_truncated:
                # 模糊匹配
                cursor.execute(
                    '''
                    SELECT id FROM chat_history 
                    WHERE created_at LIKE ? AND question LIKE ?
                    ORDER BY created_at DESC LIMIT 1
                    ''',
                    (f"{timestamp}%", f"{question_prefix}%")
                )
            else:
                # 精确匹配
                cursor.execute(
                    '''
                    SELECT id FROM chat_history 
                    WHERE created_at LIKE ? AND question = ?
                    ORDER BY created_at DESC LIMIT 1
                    ''',
                    (f"{timestamp}%", question_prefix)
                )
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return str(result[0])
            return ""
        except Exception as e:
            print(f"通过时间和问题获取记录ID时出错: {str(e)}")
            return "" 