from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_lambda_python_alpha as _alambda,
    aws_ssm as ssm,
)

class TheBetterGifterApiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Retrieve the parameter value from AWS SSM
        openai_api_key = ssm.StringParameter.value_for_secure_string_parameter(
            self, "openai-api-key", 1
        )

        print(openai_api_key)

        # Defines an AWS Lambda resource
        my_lambda = _alambda.PythonFunction(
            self, 'GiftsHandler',
            entry="./lambda/",
            runtime=_lambda.Runtime.PYTHON_3_9,
            index="gifts.py",
            handler='handler',
            timeout=Duration.seconds(30)
        )

        apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=my_lambda,
        )