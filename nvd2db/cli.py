import json

import click
import IPython

from nvd2db.core.log import set_log_level
import nvd2db.core as core


@click.group(help='')
@click.option('-l', '--log', help='log level', default='WARNING', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']))
def cli(log):
    set_log_level(log)
    

@cli.command(help='Initilize some values and database of this program for the first time.')
def init():
    core.init()


@cli.command(help='Convert NVD JSON Feed files to sqlite. Pass the files as argument to this command.')
@click.argument('inputs', nargs=-1, type=click.File(encoding='utf-8'))
def convert(inputs):
    for i in inputs:
        raw = json.loads(i.read())

        cves = raw['CVE_Items']
        rows = []
        ctr = 0
        for cve in cves:
            ctr += 1
            cve_id = cve['cve']['CVE_data_meta']['ID']
            if len(cve['impact']) == 0:
                cve_score = None
                cve_serverity = None
            else:
                cve_cvss3 = cve['impact']['baseMetricV3']['cvssV3']
                cve_score = cve_cvss3['baseScore']
                cve_serverity = cve_cvss3['baseSeverity']

            rows.append({
                'cve_id': cve_id,
                'base_score': cve_score,
                'base_severity': cve_serverity
            })

            if ctr % 1000 == 0:
                core.models.CVE.insert_many(tuple(rows)).execute()
                rows = []
        # core.models.CVE(cve_id=cve_id, base_score=cve_score, base_severity=cve_serverity).save()