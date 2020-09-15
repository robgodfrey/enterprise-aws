# Ensure Cloudwatch logs are not retained forever

Cloudwatch log groups can be configured to automatically delete logs based on a retention setting. However the default AWS retention setting for cloudwatch log groups is set to never expire events. This typically leads to cloudwatch logging costs increasing day by day as more log events are added to Cloudwatch.

### Therefore

To keep cloudwatch logging costs at a steady state relative to workload ensure that all cloudwatch log groups have specified a retention setting that isn't "Never Expire". Once a sensible retention setting is specified, log events older than the retention setting will automatically be deleted and related storage costs will no longer be incurred.

## Specifying log group retention

### Specifying log group retention in the AWS Console

You cannot specify the log group retention setting when initially creating a log group in the AWS Console. First the log groups needs to be created, and then subsequently the retention setting needs to be updated. See the AWS documentation: https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html#SettingLogRetention.

### Specifying log group retention using Cloudformation or Terraform

Both cloudformation and terraform support creation of cloudwatch log groups with a retention in days property in each case.
* https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html
* https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_group

### Bulk update existing log groups

An example python script to iterate through all log groups in all region in a single AWS account  
```python
import boto3


def boto3_client(service, region_name=None):
    """Retrieve a boto3 client for the specified service and region (if supplied)."""
    if region_name:
        return boto3.client(service, region_name=region_name)
    else:
        return boto3.client(service)


def regions():
    """Retrieve a list if AWS regions."""
    response = boto3_client("ec2").describe_regions()
    return [region["RegionName"] for region in response["Regions"]]


def update_log_group_retention_setting(logs_client, log_group_name, retention_in_days):
    logs_client.put_retention_policy(logGroupName=log_group_name, retentionInDays=retention_in_days)
    print("Updated retention setting for log group '{}' to {} days.".format(log_group_name, retention_in_days))


def all_log_groups(logs_client):
    all_log_groups = []
    paginator = logs_client.get_paginator("describe_log_groups")

    page_iterator = paginator.paginate()

    for page in page_iterator:
        all_log_groups.extend(page["logGroups"])

    return all_log_groups


def set_retention_period_for_never_expiring_log_groups(region_name, retention_in_days):
    print("Processing log groups in region '{}'.".format(region_name))

    logs_client = boto3_client("logs", region_name=region_name)

    for log_group in all_log_groups(logs_client):
        if "retentionInDays" in log_group:
            continue
        else:
            update_log_group_retention_setting(logs_client, log_group["logGroupName"], retention_in_days)

    print("Processed all log groups in region '{}'.".format(region_name))


def main():

    retention_in_days = 7

    for region_name in regions():
        set_retention_period_for_never_expiring_log_groups(region_name, retention_in_days)


if __name__ == "__main__":
    main()
```

### Automate retention setting on log group creation

TODO: Example project using cloudwatch event rule

