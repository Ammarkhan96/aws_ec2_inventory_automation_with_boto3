import boto3
import csv
from datetime import datetime


def get_ec2_inventory():
    ec2 = boto3.client("ec2")

    response = ec2.describe_instances()

    instances = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:

            name = "N/A"

            for tag in instance.get("Tags", []):
                if tag["Key"] == "Name":
                    name = tag["Value"]

            instances.append({
                "InstanceId": instance.get("InstanceId", "N/A"),
                "Name": name,
                "InstanceType": instance.get("InstanceType", "N/A"),
                "State": instance["State"]["Name"],
                "PrivateIp": instance.get("PrivateIpAddress", "N/A"),
                "PublicIp": instance.get("PublicIpAddress", "N/A"),
                "AvailabilityZone": instance["Placement"]["AvailabilityZone"]
            })

    return instances


def save_report(instances):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"reports/ec2_inventory_{timestamp}.csv"

    fieldnames = [
        "InstanceId",
        "Name",
        "InstanceType",
        "State",
        "PrivateIp",
        "PublicIp",
        "AvailabilityZone"
    ]

    with open(filename, "w", newline="") as csvfile:

        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(instances)

    print(f"Report created: {filename}")


def main():

    print("Starting EC2 inventory...")

    instances = get_ec2_inventory()

    print(f"Found {len(instances)} EC2 instance(s)")

    save_report(instances)

    print("EC2 inventory completed successfully.")


if __name__ == "__main__":
    main()
