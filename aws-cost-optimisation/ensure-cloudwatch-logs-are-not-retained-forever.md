# Pattern: Ensure Cloudwatch logs are not retained forever

Cloudwatch log groups can be configured to automatically delete logs based on a retention setting. However the default AWS retention setting for cloudwatch log groups is set to never expire events. This typically leads to cloudwatch logging costs increasing day by day as more log events are added to Cloudwatch.

## Therefore

To keep cloudwatch logging costs at a steady state relative to workload ensure that all cloudwatch log groups have specified a retention setting that isn't "Never Expire". Once a sensible retention setting is specified, log events older than the retention setting will automatically be deleted and related storage costs will no longer be incurred.

## Specifying log group retention in the AWS Console

You cannot specify the log group retention setting when initially creating a log group in the AWS Console. First the log groups needs to be created, and then subsequently the retention setting needs to be updated. See the AWS documentation: https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html#SettingLogRetention.

## Specifiying log group using Cloudformation or Terraform

Both cloudformation and terraform support creation of cloudwatch log groups with a retention in days property in each case.
* https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html
* https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_group

## Bulk update existing log groups

TODO: Add bulk update script
TODO: Create serverless project

## Automate retention setting on log group creation

TODO: Example project using cloudwatch event rule

