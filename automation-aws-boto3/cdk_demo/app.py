from aws_cdk import App, Stack
from aws_cdk import aws_s3 as s3 
from pathlib import Path

class Demostack(Stack):

    def __init__(self, scope, construct_id):
        super().__init__(scope, construct_id)

        s3.Bucket(
            self, 
            'PythonforDevOpsDemo',
            versioned = True,
        ) 

app = App()
Demostack(app, 'PythonforDevOpsDemo')
app.synth()