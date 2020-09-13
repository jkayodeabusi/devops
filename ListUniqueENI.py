import json
import boto3
import boto3.session


class ListUniqueENI(object):

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
    def list_unique_eni(cls):
        ec2_client = boto3.client('ec2',
                                  region_name='us-west-2',
                                  aws_access_key_id='AKIAI62I6QXQHAFCASTA',
                                  aws_secret_access_key='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')

        eni_description = ec2_client.describe_network_interfaces()

        filters_to_apply = {
                    "filter_by_key_value": {
                        "NetworkInterfaceId": "eni-"
                    }
                }

        applied_filter_results = cls.apply_filter_by_key_value(eni_description['NetworkInterfaces'], filters_to_apply)
        print(json.dumps(applied_filter_results))


if __name__ == '__main__':
    ListUniqueENI().list_unique_eni()



