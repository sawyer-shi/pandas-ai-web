"""
PandasAI补丁模块，用于修复库中的问题
"""
import uuid
import logging

def apply_patches():
    """应用所有PandasAI补丁"""
    logging.info("正在应用PandasAI补丁...")
    
    # 修复PipelineContext的prompt_id问题
    fixed = fix_prompt_id_issue()
    if fixed:
        logging.info("✓ 成功修复PandasAI的prompt_id问题")
    else:
        logging.warning("⚠ 无法应用PandasAI的prompt_id补丁")
    
    # 修复ResponseSerializer的Series序列化问题
    fixed = fix_series_serialization_issue()
    if fixed:
        logging.info("✓ 成功修复PandasAI的Series序列化问题")
    else:
        logging.warning("⚠ 无法应用PandasAI的Series序列化补丁")
    
    logging.info("补丁应用完成")

def fix_prompt_id_issue():
    """
    修复PandasAI中PipelineContext缺少prompt_id属性的问题
    
    Returns:
        bool: 是否成功应用补丁
    """
    try:
        from pandasai.pipelines.pipeline import PipelineContext
        
        # 保存原始初始化方法
        original_init = PipelineContext.__init__
        
        # 定义新的初始化方法
        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            # 确保实例直接有prompt_id属性
            if not hasattr(self, 'prompt_id'):
                self.prompt_id = str(uuid.uuid4())
        
        # 替换初始化方法
        PipelineContext.__init__ = new_init
        
        # 额外确保其他可能的引用点也有prompt_id属性
        try:
            # 检查是否有类方法create，如果有也进行修补
            if hasattr(PipelineContext, 'create'):
                original_create = PipelineContext.create
                
                def new_create(*args, **kwargs):
                    context = original_create(*args, **kwargs)
                    if not hasattr(context, 'prompt_id'):
                        context.prompt_id = str(uuid.uuid4())
                    return context
                
                PipelineContext.create = new_create
        except Exception as e:
            logging.warning(f"应用create方法补丁失败: {str(e)}")
            
        return True
    except Exception as e:
        logging.error(f"应用prompt_id补丁失败: {str(e)}")
        return False

def fix_series_serialization_issue():
    """
    修复PandasAI对Series类型序列化的问题
    
    Returns:
        bool: 是否成功应用补丁
    """
    try:
        import pandas as pd
        from pandasai.responses.response_serializer import ResponseSerializer
        
        # 保存原始序列化方法
        original_serialize = ResponseSerializer.serialize
        original_serialize_df = ResponseSerializer.serialize_dataframe
        
        # 定义新的序列化方法，处理Series类型
        def new_serialize(result):
            if isinstance(result, dict) and 'type' in result and 'value' in result:
                if result["type"] == "dataframe":
                    # 如果是Series类型，先转换为DataFrame
                    if isinstance(result["value"], pd.Series):
                        result["value"] = result["value"].to_frame()
                    return {"content_type": "dataframe", "value": ResponseSerializer.serialize_dataframe(result["value"])}
                if result["type"] == "string":
                    return {"content_type": "response", "value": result["value"]}
                if result["type"] == "number":
                    return {"content_type": "response", "value": str(result["value"])}
                if result["type"] == "plot":
                    return {"content_type": "plot", "value": result["value"]}
            return original_serialize(result)
        
        # 定义处理DataFrame的方法，兼容Series转换
        def new_serialize_dataframe(df):
            # 如果是Series类型，转换为DataFrame
            if isinstance(df, pd.Series):
                df = df.to_frame()
            
            # 使用原始方法处理DataFrame
            return original_serialize_df(df)
        
        # 替换序列化方法
        ResponseSerializer.serialize = new_serialize
        ResponseSerializer.serialize_dataframe = new_serialize_dataframe
            
        return True
    except Exception as e:
        logging.error(f"应用Series序列化补丁失败: {str(e)}")
        return False 