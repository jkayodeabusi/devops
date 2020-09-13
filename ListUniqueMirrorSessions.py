import boto3
import pprint


class ListUniqueMirrorSessions(object):

    @classmethod
    def list_unique_mirror_sessions(cls):
        ec2_client = boto3.client('ec2',
                                  region_name='us-west-2',
                                  aws_access_key_id='AKIAI62I6QXQHAFCASTA',
                                  aws_secret_access_key='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')

        tms_description = ec2_client.describe_traffic_mirror_sessions()
        pprint.pprint(tms_description)


if __name__ == '__main__':
    ListUniqueMirrorSessions().list_unique_mirror_sessions()
