import json
import logging

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

            row = {
                'cve_id': None,
                'cwe': None,
                'v2_base_score': None,
                'v2_severity': None,
                'v3_base_score': None,
                'v3_base_severity': None,
            }
            
            cve_id = row['cve_id'] = cve['cve']['CVE_data_meta']['ID']
            try:
                row['cwe'] = cve['cve']['problemtype']['problemtype_data'][0]['description'][0]['value']
            except IndexError:
                pass
            
            if len(cve['impact']) != 0:
                try:
                    cve_cvss3 = cve['impact']['baseMetricV3']['cvssV3']
                    row['v3_base_score'] = cve_cvss3['baseScore']
                    row['v3_base_severity'] = cve_cvss3['baseSeverity']
                except KeyError:
                    logging.info(f"{cve_id} hasn't CVSS version 3")

                try:
                    cve_cvss2 = cve['impact']['baseMetricV2']
                    row['v2_base_score'] = cve_cvss2['cvssV2']['baseScore']
                    row['v2_severity'] = cve_cvss2['severity']
                except KeyError:
                    logging.info(f"{cve_id} hasn't CVSS version 2")

            rows.append(row)

            if ctr % 1000 == 0:
                core.models.CVE.insert_many(tuple(rows)).execute()
                rows = []
