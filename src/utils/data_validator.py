"""
数据验证模块
提供专业的数据质量检查和验证功能
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import re
from datetime import datetime, timedelta

class ValidationLevel(Enum):
    """验证级别枚举"""
    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"

@dataclass
class ValidationRule:
    """验证规则数据类"""
    field_name: str
    rule_type: str
    parameters: Dict[str, Any]
    description: str
    severity: str = "warning"  # error, warning, info

@dataclass
class ValidationResult:
    """验证结果数据类"""
    field_name: str
    rule_type: str
    passed: bool
    message: str
    severity: str
    affected_rows: int = 0
    sample_values: List[Any] = None

class DataValidator:
    """数据验证器类"""
    
    def __init__(self, validation_level: ValidationLevel = ValidationLevel.STANDARD):
        self.validation_level = validation_level
        self.results: List[ValidationResult] = []
        
    def validate_dataframe(self, df: pd.DataFrame) -> List[ValidationResult]:
        """验证DataFrame"""
        self.results = []
        
        # 基础验证
        self._validate_basic_structure(df)
        
        # 数据类型验证
        self._validate_data_types(df)
        
        # 数据范围验证
        self._validate_data_ranges(df)
        
        # 数据格式验证
        self._validate_data_formats(df)
        
        # 业务逻辑验证
        self._validate_business_logic(df)
        
        return self.results
    
    def _validate_basic_structure(self, df: pd.DataFrame):
        """验证基础结构"""
        # 检查是否为空
        if df.empty:
            self.results.append(ValidationResult(
                field_name="dataframe",
                rule_type="not_empty",
                passed=False,
                message="数据框为空",
                severity="error"
            ))
        
        # 检查列名
        for col in df.columns:
            if not isinstance(col, str):
                self.results.append(ValidationResult(
                    field_name=col,
                    rule_type="column_name_type",
                    passed=False,
                    message=f"列名 '{col}' 不是字符串类型",
                    severity="error"
                ))
            
            # 检查列名格式
            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', str(col)):
                self.results.append(ValidationResult(
                    field_name=col,
                    rule_type="column_name_format",
                    passed=False,
                    message=f"列名 '{col}' 格式不符合规范",
                    severity="warning"
                ))
    
    def _validate_data_types(self, df: pd.DataFrame):
        """验证数据类型"""
        for col in df.columns:
            # 检查数据类型一致性
            non_null_values = df[col].dropna()
            if len(non_null_values) > 0:
                # 检查数值型列
                if df[col].dtype in ['int64', 'float64']:
                    if not all(isinstance(x, (int, float, np.integer, np.floating)) for x in non_null_values):
                        self.results.append(ValidationResult(
                            field_name=col,
                            rule_type="numeric_consistency",
                            passed=False,
                            message=f"列 '{col}' 包含非数值型数据",
                            severity="error"
                        ))
                
                # 检查日期型列
                elif df[col].dtype == 'datetime64[ns]':
                    if not all(isinstance(x, (datetime, pd.Timestamp)) for x in non_null_values):
                        self.results.append(ValidationResult(
                            field_name=col,
                            rule_type="datetime_consistency",
                            passed=False,
                            message=f"列 '{col}' 包含非日期型数据",
                            severity="error"
                        ))
    
    def _validate_data_ranges(self, df: pd.DataFrame):
        """验证数据范围"""
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64']:
                values = df[col].dropna()
                if len(values) > 0:
                    # 检查异常值
                    Q1 = values.quantile(0.25)
                    Q3 = values.quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    
                    outliers = values[(values < lower_bound) | (values > upper_bound)]
                    if len(outliers) > 0:
                        self.results.append(ValidationResult(
                            field_name=col,
                            rule_type="outlier_detection",
                            passed=False,
                            message=f"列 '{col}' 包含 {len(outliers)} 个异常值",
                            severity="warning",
                            affected_rows=len(outliers),
                            sample_values=outliers.head(5).tolist()
                        ))
                    
                    # 检查负值（如果业务上不允许）
                    if self.validation_level == ValidationLevel.STRICT:
                        negative_values = values[values < 0]
                        if len(negative_values) > 0:
                            self.results.append(ValidationResult(
                                field_name=col,
                                rule_type="negative_values",
                                passed=False,
                                message=f"列 '{col}' 包含 {len(negative_values)} 个负值",
                                severity="warning",
                                affected_rows=len(negative_values)
                            ))
    
    def _validate_data_formats(self, df: pd.DataFrame):
        """验证数据格式"""
        for col in df.columns:
            if df[col].dtype == 'object':
                values = df[col].dropna()
                if len(values) > 0:
                    # 检查字符串长度
                    if self.validation_level in [ValidationLevel.STANDARD, ValidationLevel.STRICT]:
                        max_length = values.astype(str).str.len().max()
                        if max_length > 1000:
                            self.results.append(ValidationResult(
                                field_name=col,
                                rule_type="string_length",
                                passed=False,
                                message=f"列 '{col}' 包含超长字符串（最大长度: {max_length}）",
                                severity="warning"
                            ))
                    
                    # 检查特殊字符
                    if self.validation_level == ValidationLevel.STRICT:
                        special_chars = values.astype(str).str.contains(r'[^\w\s\-\.]', regex=True)
                        if special_chars.any():
                            self.results.append(ValidationResult(
                                field_name=col,
                                rule_type="special_characters",
                                passed=False,
                                message=f"列 '{col}' 包含特殊字符",
                                severity="info",
                                affected_rows=special_chars.sum()
                            ))
    
    def _validate_business_logic(self, df: pd.DataFrame):
        """验证业务逻辑"""
        # 这里可以根据具体业务需求添加验证规则
        pass
    
    def add_custom_rule(self, rule: ValidationRule, df: pd.DataFrame):
        """添加自定义验证规则"""
        if rule.rule_type == "unique":
            duplicates = df[rule.field_name].duplicated()
            if duplicates.any():
                self.results.append(ValidationResult(
                    field_name=rule.field_name,
                    rule_type=rule.rule_type,
                    passed=False,
                    message=rule.description,
                    severity=rule.severity,
                    affected_rows=duplicates.sum()
                ))
        
        elif rule.rule_type == "range":
            min_val = rule.parameters.get('min')
            max_val = rule.parameters.get('max')
            values = df[rule.field_name].dropna()
            
            if min_val is not None:
                below_min = values[values < min_val]
                if len(below_min) > 0:
                    self.results.append(ValidationResult(
                        field_name=rule.field_name,
                        rule_type=rule.rule_type,
                        passed=False,
                        message=f"{rule.description} - 值小于最小值 {min_val}",
                        severity=rule.severity,
                        affected_rows=len(below_min)
                    ))
            
            if max_val is not None:
                above_max = values[values > max_val]
                if len(above_max) > 0:
                    self.results.append(ValidationResult(
                        field_name=rule.field_name,
                        rule_type=rule.rule_type,
                        passed=False,
                        message=f"{rule.description} - 值大于最大值 {max_val}",
                        severity=rule.severity,
                        affected_rows=len(above_max)
                    ))
        
        elif rule.rule_type == "pattern":
            pattern = rule.parameters.get('pattern')
            if pattern:
                values = df[rule.field_name].dropna()
                invalid_values = values[~values.astype(str).str.match(pattern)]
                if len(invalid_values) > 0:
                    self.results.append(ValidationResult(
                        field_name=rule.field_name,
                        rule_type=rule.rule_type,
                        passed=False,
                        message=f"{rule.description} - 格式不匹配",
                        severity=rule.severity,
                        affected_rows=len(invalid_values),
                        sample_values=invalid_values.head(5).tolist()
                    ))
    
    def get_summary(self) -> Dict[str, Any]:
        """获取验证摘要"""
        if not self.results:
            return {"message": "未进行验证"}
        
        total_rules = len(self.results)
        passed_rules = sum(1 for r in self.results if r.passed)
        failed_rules = total_rules - passed_rules
        
        error_count = sum(1 for r in self.results if r.severity == "error" and not r.passed)
        warning_count = sum(1 for r in self.results if r.severity == "warning" and not r.passed)
        info_count = sum(1 for r in self.results if r.severity == "info" and not r.passed)
        
        return {
            "total_rules": total_rules,
            "passed_rules": passed_rules,
            "failed_rules": failed_rules,
            "pass_rate": (passed_rules / total_rules) * 100 if total_rules > 0 else 0,
            "error_count": error_count,
            "warning_count": warning_count,
            "info_count": info_count,
            "validation_level": self.validation_level.value
        }

class EmailValidator:
    """邮箱验证器"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """验证邮箱格式"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_email_column(df: pd.DataFrame, column: str) -> List[ValidationResult]:
        """验证邮箱列"""
        results = []
        values = df[column].dropna()
        
        invalid_emails = []
        for email in values:
            if not EmailValidator.validate_email(str(email)):
                invalid_emails.append(email)
        
        if invalid_emails:
            results.append(ValidationResult(
                field_name=column,
                rule_type="email_format",
                passed=False,
                message=f"列 '{column}' 包含 {len(invalid_emails)} 个无效邮箱",
                severity="error",
                affected_rows=len(invalid_emails),
                sample_values=invalid_emails[:5]
            ))
        
        return results

class PhoneValidator:
    """电话验证器"""
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """验证电话号码格式"""
        # 支持多种格式：+86-138-1234-5678, 13812345678, 138-1234-5678
        pattern = r'^(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}$'
        return bool(re.match(pattern, str(phone)))
    
    @staticmethod
    def validate_phone_column(df: pd.DataFrame, column: str) -> List[ValidationResult]:
        """验证电话列"""
        results = []
        values = df[column].dropna()
        
        invalid_phones = []
        for phone in values:
            if not PhoneValidator.validate_phone(str(phone)):
                invalid_phones.append(phone)
        
        if invalid_phones:
            results.append(ValidationResult(
                field_name=column,
                rule_type="phone_format",
                passed=False,
                message=f"列 '{column}' 包含 {len(invalid_phones)} 个无效电话号码",
                severity="error",
                affected_rows=len(invalid_phones),
                sample_values=invalid_phones[:5]
            ))
        
        return results

# 便捷函数
def validate_dataframe(df: pd.DataFrame, level: ValidationLevel = ValidationLevel.STANDARD) -> List[ValidationResult]:
    """验证DataFrame"""
    validator = DataValidator(level)
    return validator.validate_dataframe(df)

def get_validation_summary(results: List[ValidationResult]) -> Dict[str, Any]:
    """获取验证摘要"""
    validator = DataValidator()
    validator.results = results
    return validator.get_summary()

def create_custom_rule(field_name: str, rule_type: str, parameters: Dict[str, Any], 
                      description: str, severity: str = "warning") -> ValidationRule:
    """创建自定义验证规则"""
    return ValidationRule(
        field_name=field_name,
        rule_type=rule_type,
        parameters=parameters,
        description=description,
        severity=severity
    )
