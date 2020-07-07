from aws_cdk import (
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_sqs as sqs, 
    core
)

class PlaygroundStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        dispatcher = sns.Topic(self, 'TestDispatcher')
        core.CfnOutput(self, 'testDispatcher',
            value=dispatcher.topic_arn,
            export_name='testDispatcherArn'
        )

        for queueName in ['q1', 'q2', 'q3', 'q4']:
            q = sqs.Queue(self, queueName)
            dispatcher.add_subscription(subscriptions.SqsSubscription(q,
                raw_message_delivery=True,
            ))

            core.CfnOutput(self, f'{queueName}Url',
                value=q.queue_url,
                export_name=f'{queueName}Url'
            )
