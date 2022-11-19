from peewee import CharField, FloatField

from nvd2db.core.database import BaseModel


class CVE(BaseModel):
    cve_id = CharField(unique=True)
    base_score = FloatField(null=True)
    base_severity = CharField(null=True)