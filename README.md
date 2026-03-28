# README #

* Quick Summary

The Milliman IntelliScript Machine Learning Engineer Exam.

## Repo Overview ##

* Folder Summary

- src
  - ml_engineer_exam
    - model
      - The module needed to train and evaluate the model
    - prediction
      - The module needed to make predictions with the trained model
    - prepare
      - The module needed to prepare the data for training and evaluation
    - scripts
      - run_model_training.py
        - Trains a model ('linear', 'ridge', 'random_forest') using the California housing dataset.
      - run_prediction.py
        - Makes predictions using a trained model and sample input data.
    - config.py
      - Config classes for model training and prediction

### How do I get set up? ###

* Pre-requisites (local running)
  - [Setup SSH Keys needed to pull down repositories](https://www.atlassian.com/git/tutorials/git-ssh)
  - [Install UV](https://docs.astral.sh/uv/getting-started/installation/)

* Repo-setup

- Clone Repo (in IDE)
- Setup UV Environment
  ```shell
  uv sync
  ```

### Code Tests ###
Code testing lives in the `tests` folder at the root directory. Add any tests here and run the following code to test.

```shell
uv run pytest -v
```

## Running Code ##
There are 4 ways to run the code in this repository
1. Run the scripts manually
2. Run the app using FastAPI locally
3. Manually deploying the container and models to AWS
4. GHA deploy of the container through the API Gateway

#### 1. Run Scripts Manually ####

  - Run Command
  ```shell
  uv run run_model_training --model_type linear
  uv run run_prediction --model_name linear --input_data "{\"MedInc\": 1.6812, \"HouseAge\": 25.0, \"AveRooms\": 4.192200557103064, \"AveBedrms\": 1.0222841225626742, \"Population\": 1392.0, \"AveOccup\": 3.877437325905293, \"Latitude\": 36.06, \"Longitude\": -119.01}"
  ```
#### 2. Run App Locally Using FastAPI ####
  Move into FastAPI directory
  - `cd src/ml_engineer_exam/api`

  Run the application
  - `uv run python -m app`

  ##### Access FastAPI through SwaggerAPI
  - Go to http://localhost:8080/docs in your browser

  ##### Access API using Terminal Commands to Check
  - Health check
  ```shell
  curl -X 'GET' \
  'http://localhost:8080/ping' \
  -H 'accept: application/json'
  ```
  - Train Model
    ```shell
  curl -X 'POST' \
  'http://localhost:8080/train' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "model_name": "linear"
  }'
  ```

  - Predict
    1. Use the JSON file directly with curl:
  ```shell
  curl -X POST http://localhost:8080/predict \
    -H "Content-Type: application/json" \
    -d @src/ml_engineer_exam/api/predict_request.json
  ```

    2. Override just what you need (note that defaults live in `src/ml_engineer_exam/api/app.py`):
  ```shell
  curl -X POST http://localhost:8080/predict \
    -H "Content-Type: application/json" \
    -d '{"MedInc": 2.5, "model_name": "ridge"}'
  ```

#### 3. Manually Deploying to AWS Lambda and API Gateway ####
Prerequisites:
1) AWS CLI installed and configured with policies for IAM, ECR, Lambda, and API Gateway. Update the IAM in terraform to point to your forked repository.
2) Terraform and Docker installed
3) Models trained locally in data/models/ directory

Rebuild the docker container for AWS-compatible linux
```docker buildx build --platform linux/amd64 --provenance=false -t ml-model-deployment:v1 .```

Test and validate infrastructure on your machine:
```cd terraform```
```terraform init```
```terraform validate```
```terraform plan```

Set up ECR Repository that you can push the Docker Container to:
```terraform apply -target=aws_ecr_repository.housing_model```

This will output an ECR Repository URL - save this in an environment variable:
```export ECR_URL=<YOUR_URL_HERE>```
```aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_URL```

Tag and push the image to ECR:
```cd ..```
```docker tag ml-model-deployment:v1 ${ECR_URL}:v1```
```docker push ${ECR_URL}:v1```

Build the IAM, Lambda, API Gateway, and ECR instance:
```cd terraform```
```terraform apply```

You should see a message `Apply complete! Resources: 5 added, 0 changed, 0 destroyed.`

##### Testing Your API GATEWAY #####
Use the `api_gateway_url` output from your terraform apply:
```export API_GATEWAY_URL=<your_url_here>```

Ping the endpoint for a health check:
```curl $API_GATEWAY_URL/ping```

Make a prediction:
```shell
curl -X POST $API_GATEWAY_URL/predict \
  -H "Content-Type: application/json" \
  -d '{"model_name": "linear", "MedInc": 2.5}'
```

#### 4. Deploy via GitHub Actions ####
Prerequisites:
1) Completed step 3 at least once to provision AWS infrastructure
2) Your own GitHub repo forked from this one with GHA enabled
3) GitHub `production` environment configured with yourself as a required reviewer under Settings → Environments → production. This prevents others from making changes to your repo and accessing your cloud resources


After `terraform apply`, save the following as repository variables in your GitHub repo under Settings → Secrets and variables → Actions → Variables so that the `deploy.yml` script can read your secrets:

`ECR_REGISTRY`, `123.dkr.ecr.us-east-1.amazonaws.com`
`ECR_REPOSITORY`, `123.dkr.ecr.us-east-1.amazonaws.com/my-ml-model`
`AWS_ROLE_ARN`, `arn:aws:iam::123:role/GitHubActionsDeployRole`

Pushes to `main` will trigger the deploy workflow and wait for approval before running. Go into "Actions" in Github to approve the production deployment.

## Notes from Ben ##
API specific next steps
- Standardize predictions using pydantic, add max/min on prediction request variables, make sure that there are no nulls, and establish default variable values and error handling
- Build datacapture to track user inputs to the API to use for model training
- Build API performance analytics in Datadog
- Work with product to see how this API fits in with other system teams
- Initially I had written a dockerfile for testing locally. I overwrote this with AWS-compatible Dockerfile. Rewrite the original local DockerFile and have a dockerfiles folder

Infrastructure next steps
- Add policies for image lifecycle, i.e. spin down images 2 days old or spin down the oldest image when more than 3 have been deployed
- Set up atlantis to plan and deploy on github PRs, allowing for terraform applying and planning on Github
- Add more formatting around cloudwatch logs and handling
- Write all of the locally run terraform to . Combine steps 3 and 4 of "Running the code" to run terraform apply in the GHA and provision ECR

Repo design ideas
- Increase pytest rigorour around the rest of the package. i.e. what if there is no model in the container? What if the container breaks? How do we pass through useful 200s, 400s, and 500s to the user through the API?
- Split the `run_model` function into 3 different API calls - `/get_data`, `/train_model` and `/evaluate_model`
- Consolidate one-line functions into larger more modular functions
- Decide where functional vs OOP design fits in here (my take is functional if it's only being run in one place)
- Move these runner functions out of the init files
- Potentially un-abbreviate variable names to make it easier for future readers, i.e. id could be identification, primary key, input data

### Contribution guidelines ###

* Code review

All code reviews should be attached to a merge request or equivalent in your version control system
(e.g. merge requests are called pull requests in bitbucket)

* Other guidelines

- Add doc strings (preferable restStructuredText)
- Use an IDE like Pycharm, Visual Studio Code,
- Follow PEP standards
- Create new branches for any work that you do
- Make sure to bump the project version

  ```bash
  uv version --bump minor #patch or minor or major
  ```

### Who do I talk to? ###

* Dependencies

The project dependencies are located in the pyproject.toml file.
You can see them by running a pip command "pip show ml_engineer_exam" after installing the package via uv.

* Repo owner or admin

Contact nicholas.arquette@milliman.com
API and cloud infra developer ben.s.merrill@gmail.com
