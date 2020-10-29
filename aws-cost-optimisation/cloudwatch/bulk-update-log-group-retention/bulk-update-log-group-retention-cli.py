import boto3


def main():
    update_retention_period_for_never_expiring_log_groups_in_all_regions(retention_in_days=7)


def update_retention_period_for_never_expiring_log_groups_in_all_regions(retention_in_days):
    for region_name in all_regions():
        update_retention_period_for_never_expiring_log_groups(region_name, retention_in_days)


def update_retention_period_for_never_expiring_log_groups(region_name, retention_in_days):
    print("Processing log groups in region '{}' ...".format(region_name))

    logs_client = boto3.client("logs", region_name=region_name)

    for log_group in all_log_groups(logs_client):
        if "retentionInDays" not in log_group:
            update_log_group_retention_setting(logs_client, log_group["logGroupName"], retention_in_days)

    print("Processed all log groups in region '{}'.".format(region_name))


def update_log_group_retention_setting(logs_client, log_group_name, retention_in_days):
    logs_client.put_retention_policy(logGroupName=log_group_name, retentionInDays=retention_in_days)
    print(" - Updated retention setting for log group '{}' to {} days.".format(log_group_name, retention_in_days))


def all_regions():
    response = boto3.client("ec2").describe_regions()
    return [region["RegionName"] for region in response["Regions"]]


def all_log_groups(logs_client):
    all_log_groups = []
    paginator = logs_client.get_paginator("describe_log_groups")

    for page in paginator.paginate():
        all_log_groups.extend(page["logGroups"])

    return all_log_groups


if __name__ == "__main__":
    main()
