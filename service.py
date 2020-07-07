import boto3
from multiprocessing import Process, Manager
from pprint import pprint

session = boto3.session.Session(
    region_name='us-west-1',
    profile_name='prod'
)

class Worker():

    def __init__(self, queueUrl):
        self.queueUrl = queueUrl

    def process(self):
        try:
            queue = session.resource('sqs').Queue(self.queueUrl)
            while True:
                print(f'Getting messages for {queue.url}')
                messages = queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=20)
                for message in messages:
                    print(message.body)
                    message.delete()

        except KeyboardInterrupt:
            print(f'Received keyboard interrupt for {queue.url}')
        finally:
            print(f'Cleaning up for {queue.url}')
    
def work(worker):
    worker.process()
        
if __name__ == '__main__':

    # Get the list of queues from the CF outputs
    outputs = session.client('cloudformation').describe_stacks(StackName='playground')['Stacks'][0]['Outputs']
    queueUrls = [ x['OutputValue'] for x in outputs if x['OutputKey'].startswith('q') ]

    pprint(queueUrls)
    
    workers = []
    manager = Manager()
    for queueUrl in queueUrls:
        worker = Worker(queueUrl)
        p = Process(target=work, args=(worker,))
        p.start()
        workers.append(p)

    