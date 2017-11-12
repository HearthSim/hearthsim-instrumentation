import os


def get_secure_parameters(namespace: str, debug: bool=False) -> dict:
	if debug:
		return os.environ

	import boto3

	ssm = boto3.client("ssm")

	prefix = "/{}/".format(namespace)
	kwargs = {"Path": prefix, "Recursive": True, "WithDecryption": True}
	response = ssm.get_parameters_by_path(**kwargs)

	params = list(response["Parameters"])
	while response.get("NextToken"):
		kwargs["NextToken"] = response["NextToken"]
		response = ssm.get_parameters_by_path(**kwargs)
		params += response["Parameters"]

	ret = {}
	for p in params:
		ret[p["Name"].replace(prefix, "").upper()] = p["Value"]

	return ret
