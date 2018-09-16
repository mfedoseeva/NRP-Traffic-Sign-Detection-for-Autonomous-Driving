loading the street environment:

1. please make sure you have already added our assets into NRP. If no, refer to README in the Assets folder

2. add street.sdf into your experiment folder

3. find the file "experiment_configuration.exc" in your experiment folder. this line: \<environmentModel src=...\> defines the environment you are using, edit it into:  \<environmentModel src="street.sdf"\> 

3. (optional) if you can't load the environment, use model_library.json in this folder. You should repeat all the steps from the beginning(including adding assets). 
