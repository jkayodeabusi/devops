import json
import boto3
import boto3.session


class ManageNetworkTraffic(object):

    @classmethod
    def apply_filter_by_key_value(cls, eni_data, element):
        filter_by_key_value = element['filter_by_key_value']
        filtered_page = []
        for eni_row in eni_data:
            # remove any datetime field
            if 'Attachment' in eni_row.keys():
                attachment = eni_row['Attachment']
                attachment.pop('AttachTime')
                eni_row.update({"Attachment": attachment})

            formatted = json.dumps(eni_row)
            loaded_r = json.loads(formatted)

            for key in filter_by_key_value.keys():
                value = filter_by_key_value[key]
                if str(key).lower() in dict(loaded_r).keys().__str__().lower() and str(loaded_r[key]).lower().\
                        startswith(str(value).lower()):
                    row = dict()
                    if 'Attachment' in eni_row.keys() and 'InstanceId' in eni_row['Attachment'].keys():
                        row.update({"InstanceId": eni_row["Attachment"]["InstanceId"]})
                        row.update({"NetworkInterfaceId": eni_row["NetworkInterfaceId"]})
                        row.update({"VpcId": eni_row["VpcId"]})
                        row.update({"OwnerId": eni_row["OwnerId"]})
                        filtered_page.append(row)
                    eni_data = filtered_page

        return eni_data

    @classmethod
    def create_traffic_mirror_session(cls):
        ec2_client = boto3.client('ec2',
                                  region_name='us-west-2',
                                  aws_access_key_id='AKIAI62I6QXQHAFCASTA',
                                  aws_secret_access_key='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')

        eni_description = ec2_client.describe_network_interfaces()
        tms_description = ec2_client.describe_traffic_mirror_sessions()

        tms_description = tms_description['TrafficMirrorSessions']
        filters_to_apply = {
                    "filter_by_key_value": {
                        "NetworkInterfaceId": "eni-"
                    }
                }

        applied_filter_results = cls.apply_filter_by_key_value(eni_description['NetworkInterfaces'], filters_to_apply)

        def exec_mst(session_record):
            ec2_client.create_traffic_mirror_session(
                NetworkInterfaceId=session_record['NetworkInterfaceId'],
                TrafficMirrorTargetId='tmt-06e89cd1d0b96b04b',
                TrafficMirrorFilterId='tmf-07a199e9fc5e6b745',
                SessionNumber=1,
            )

        for result in applied_filter_results:
            if bool(tms_description):
                for mrt in tms_description:
                    if 'NetworkInterfaceId' in mrt.keys() and mrt['NetworkInterfaceId'] == result['NetworkInterfaceId'] \
                            and 'OwnerId' in mrt.keys() and mrt['OwnerId'] == result['OwnerId']:
                        print('skipping...')
                        pass
                    else:
                        try:
                            exec_mst(result)
                        except Exception as e:
                            if str(e).__contains__('is in use by target'):
                                continue
            else:
                try:
                    exec_mst(result)
                except Exception as e:
                    if str(e).__contains__('is in use by target'):
                        continue

        print('done')


if __name__ == '__main__':
    ManageNetworkTraffic().create_traffic_mirror_session()



