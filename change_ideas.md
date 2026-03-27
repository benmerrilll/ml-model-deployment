Ideas
- Move these runner functions out of the init files


Questions
- Why are there one-line functions? Should we move these into larger more modular functions?
- What was the idea behind classes?
- Why abbreviate? Descriptive tokens are usually really helpful -> i.e. id - identification, primary key, input data
- I really want to split the `run_model` function into 3 different API calls - `/get_data`, `/train_model` and `/evaluate_model`
    - This could give us the ability to load a model and predict
- Load the model in the initialzation of predict.
- I bypassed the scripts folder and pulled that code into the `app.py` file to have health check, train, and predict all in the same file for a single API deployment
- Error handling, what if the model is not there? What if the container breaks, how do we pass through 200s, 400s, and 500s to the user
- To standardize the predictions, add max/min on prediction request variables, make sure that there are no nulls, and establish default variable values

- Add cloudwatch logs
- Add policy for image lifecycle, i.e. spin up and spin down images
- Integrate with other system teams
- Set up atlantis to plan and deploy on your github PRs
