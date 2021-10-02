# Use the Reddit API to read posts from a subreddit and store them in a database on anhourly schedule
## A Kinesis Firehose, S3, Glue, Athena Use-case

### Updated October 2021

----

## Table of Contents

1. Create your Reddit bot account
2. Set up an S3 Bucket
3. Deploy the AWS Glue data catalog in CloudFormation
4. Set up Kinesis Firehose Delivery Stream
5. Create a Key Pair for your streaming server
6. Deploy the EC2 streaming server in CloudFormation
7. Monitor the delivery stream
8. Use Athena to develop insights


## 1. Create your Reddit bot account

1. [Register a reddit account](https://www.reddit.com/register/)

2. Follow prompts to create new reddit account:
    * Provide email address
    * Choose username and password
    * Click Finish

3. Once your account is created, go to [reddit developer console.](https://www.reddit.com/prefs/apps/)

4. Select **“are you a developer? Create an app...”**

5. Give it a name.

6. Select script.  <--- **This is important!**

7. For about url and redirect uri, use http://127.0.0.1

8. You will now get a client_id (underneath web app) and secret

9. Keep track of your Reddit account username, password, app client_id (in blue box), and app secret (in red box). These will be used in tutorial Step 11


### Next steps: S3

* Our app information is registered now. Before you begin setting up the server or the delivery stream, you need a place to store the data that will be generated.

----

## 5. Set up an S3 Bucket

1. Open the [Amazon S3 console](https://console.aws.amazon.com/s3/)

2. Choose Create bucket

3. In the Bucket name field, type a unique DNS-compliant name for your new bucket. Create your own bucket name using the following naming guidelines:

    * The name must be unique across all existing bucket names in Amazon S3

    * Example: reddit-analytics-bucket-\<add random number here>

    * After you create the bucket you cannot change the name, so choose wisely

    * Choose a bucket name that reflects the objects in the bucket because the bucket name is visible in the URL that points to the objects that you're going to put in your bucket

    * For information about naming buckets, see Rules for Bucket Naming in the Amazon Simple Storage Service Developer Guide

4. For Region, choose US East (N. Virginia) as the region where you want the bucket to reside

5. Keep defaults and continue clicking Next

6. Choose Create

Now that you’ve created a bucket, let’s set up a delivery stream for your data.

### Next steps: Glue

* S3 is a place to store many different kinds of data / files.  To provide the data files with structure that services can reference, you need to set up a data catalog.  AWS Glue is the perfect service for this use case.

----

## 6. Deploy the AWS Glue data catalog in CloudFormation

In this step we will be using a tool called CloudFormation.  Instead of going through the AWS console and creating glue databases and glue tables click by click, we can utilize CloudFormation to deploy the infrastructure quickly and easily.

We will use Cloudformation YAML templates located in this GitHub repository

1. Go to the glue.yml file located [here](https://github.com/Gireeshsit/Pelago-Assignment/blob/main/glue.yml)

2. Right-click anywhere and select Save as…

3. Rename the file from glue.txt to glue.yml

4. Select All Files as the file format and select Save

5. Open the [AWS CloudFormation console](https://console.aws.amazon.com/cloudformation)

6. If this is a new AWS CloudFormation account, click Create New Stack Otherwise, click Create Stack

7. In the Template section, select Upload a template file

8. Select Choose File and upload the newly downloaded glue.yml template

9. Decide on your stack name

10. Under pBucketName set your bucket name from the previous step

11. Continue until the last step and click Create stack

12. Click on Events tab. Wait until the stack status is CREATE_COMPLETE


### Next steps: Kinesis Firehose

* Now you have a destination for your data (S3) and a data catalog (AWS Glue).  Next, let’s deploy the pipes that will allow data to travel between services.

----

## 7. Set up Kinesis Firehose Delivery Stream

1. Open the [Kinesis Data Firehose console](https://console.aws.amazon.com/firehose/) or select Kinesis in the Services dropdown

2. Choose Create Delivery Stream

3. Delivery stream name – Type a name for the delivery stream

    Example: raw-reddit-comment-delivery-stream

4. Keep default settings on Step 1 - you will be using a direct PUT as source. Scroll down and click Next

5. In Step 2, enable record format conversion by using the following settings:

6. Click Next

7. On the Destination page, choose the following options
    * Destination – Choose Amazon S3

    * S3 bucket – Choose an existing bucket created in tutorial Step 6

    * S3 prefix – add "raw_reddit_comments/" as prefix

    * S3 error prefix - add "raw_reddit_comments_error/" as prefix

8. Choose Next

9. On the Configuration page, Change Buffer time to 60 seconds

10. For IAM Role, click Create new or choose

11. For the IAM Role summary, use the following settings:

12. Choose Allow

13. You should return to the Kinesis Data Firehose delivery stream set-up steps in the Kinesis Data Firehose console

14. Choose Next

15. On the Review page, review your settings, and then choose Create Delivery Stream

### Next steps: EC2

* The pipeline and destination are now available for use.  In the next several steps, you will be creating the python application that generates Reddit comment data.

----

## 8. Create a Key Pair for your streaming server

1. Open the [Amazon EC2 console](https://console.aws.amazon.com/ec2/) or select EC2 under Services dropdown

2. In the navigation pane, under NETWORK & SECURITY, choose Key Pairs

    Note: The navigation pane is on the left side of the Amazon EC2 console. If you do not see the pane, it might be minimized; choose the arrow to expand the pane

3. Choose Create Key Pair

4. For Key pair name, enter a name for the new key pair (ex: RedditBotKey), and then choose Create

5. The private key file is automatically downloaded by your browser. The base file name is the name you specified as the name of your key pair, and the file name extension is .pem. Save the private key file in a safe place



### Next steps: Cloudformation

A key pair will allow you to securely access a server. In the next steps, you will deploy the server.

----

## 9. Deploy the EC2 streaming server in CloudFormation

In this step you will be using a tool called CloudFormation.  Instead of going through the AWS console and creating an EC2 instance click by click, you can utilize CloudFormation to deploy the infrastructure quickly.  This CloudFormation template has EC2 user data to set up the machine. The EC2 user data achieves the following:

* Installs python 3.6 and several libraries needed for the script to run
* Clones a GitHub repository that contains the python script
* Updates python script with custom permissions and parameters
* Executes the script to begin the data stream

We will use Cloudformation YAML templates located in this GitHub repository.

1. Go to the ec2.yml file located [here.](https://github.com/Gireeshsit/Pelago-Assignment/blob/main/ec2.yml)

2. Right-click anywhere and select Save as…

3. Rename the file from ec2.txt to ec2.yml

4. Select All Files as the file format and select Save

5. Open the [AWS CloudFormation console](https://console.aws.amazon.com/cloudformation) or select CloudFormation under the Services dropdown

6. Click Create New Stack / Create Stack

7. In the Template section, select Upload a template file

8. Select Choose File and upload the newly downloaded ec2.yml template

9. Click Next

10. Provide a stack name (ex: reddit-stream-server)

11. For pKeyName and provide the key name that you created in tutorial Step 9

12. Use your reddit app info and reddit account for the parameters pRedditAppSecret, pRedditClientID, pRedditUsername, and pRedditPassword

13. You can choose to leave the rest of the parameters as their default values.

14. Continue to click Next

15. On the last step, acknowledge IAM resource creation and click Create Stack

16. Wait for your EC2 instance to be created.

17. Make a note of the Public IP and Public DNS Name given to the newly created instance.  You can find these in the Cloudformation Outputs tab.

18. Open the [Amazon EC2 console](https://console.aws.amazon.com/ec2/) or select EC2 under Services dropdown

19. Select INSTANCES in the navigation pane

20. Ensure that an EC2 instance has been created and running. (This can take several minutes to deploy)

### Next steps: Monitoring Kinesis Firehose

* Now that the EC2 instance is provisioned and the script is running, the data is streaming to Kinesis Firehose. In the next step we’ll monitor the data as it moves through the delivery stream and into S3.

----

## 10. Monitor the delivery stream

1. Open the [Amazon Kinesis Firehose console](https://console.aws.amazon.com/firehose/) or select Kinesis in the Services dropdown

2. Select the delivery stream created in step 8.

3. Select Monitoring Tab

4. Click refresh button over the next 3 minutes. You should start to see records coming in

5. If you are still not seeing data after 3-5 minutes, go to Appendix I for troubleshooting.

6. Now let’s check the S3 bucket

7. Open the [Amazon S3 console](https://console.aws.amazon.com/s3/) or select S3 in the Services dropdown

8. Click the bucket name of the bucket that you created in step 2

9. Verify that records are being PUT into your s3 bucket

Now that data is streaming into s3, let’s build a data catalog so that you can query our s3 files



## 11. Use Athena to develop insights

1. Open the [Amazon Athena console](https://console.aws.amazon.com/athena/) or select Athena in the Services dropdown

2. Choose the glue database (reddit_glue_db) populated on the left view

3. Select the table (raw_reddit_comments) to view the table schema

4. You should now be able to use SQL to query the table (S3 data)

    