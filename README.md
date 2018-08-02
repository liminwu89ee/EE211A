# UCLA Electrical Engineering - EE211A Digital Image Processing Project (Remasted version)
by Limin Wu, Qi Wang

This code is not final, we are still working on it for better performance.

Read me first!
General work flow:
1. modify and run writeConfig.py to set global parameters.
2. run main_generate3D to convert SWC files(in "input" folder)  to 3D matrix (in "matrix3D" folder).
3. run main_generate2Dimages.py to generate dummy X-ray images with center line extracted.
4. run main_generateTraining.py to generate training set in csv format (in "data" folder).
5. run main_training.py to generate model.
6. run main_prediction.py to generate reconstructed 3D model from dummy X-ray images.
7. run main_generateView.py to generate different views of ground-truth 3D model and reconstructed 3D model.
8. run main_validation.py to evaluate the result
