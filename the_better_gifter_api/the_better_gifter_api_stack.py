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
        # Currently lambda does not support value_for_secure_string from ssm param store
        openai_secret_api_key = ssm.StringParameter.value_for_string_parameter(
            self, "openai-secret-key"
        )

        # Defines an AWS Lambda resource
        my_lambda = _alambda.PythonFunction(
            self, 'GiftsHandler',
            entry="./lambda/",
            runtime=_lambda.Runtime.PYTHON_3_9,
            index="gifts.py",
            handler='handler',
            timeout=Duration.seconds(30),
            environment={
                "OPENAI_API_KEY": openai_secret_api_key
            }
        )

        apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=my_lambda,
            default_cors_preflight_options={
                "allow_origins": apigw.Cors.ALL_ORIGINS,
                "allow_methods": apigw.Cors.ALL_METHODS,
                "allow_headers": ["Content-Type"],
                "max_age": Duration.days(1)
            }
        )
