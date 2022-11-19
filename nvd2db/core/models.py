from peewee import CharField, FloatField, ForeignKeyField

from nvd2db.core.database import BaseModel


    
class CVE(BaseModel):
    cve_id = CharField(unique=True)
    cwe = CharField(null=True)
    v2_base_score = FloatField(null=True)
    v2_severity = CharField(null=True)
    v3_base_score = FloatField(null=True)
    v3_base_severity = CharField(null=True)
