# Easy transformation and scaling of DeepLabCut Data

#### Background
DeepLabCut is a widely used markerless pose estimation toolbox in behavioral science. The output of DeepLabCut is coordinates in pixels for each frame for each marker. However, in most cases the coordinates first need to be translated (i.e. adapted to the coordinate-space of the behavioral maze) and scaled (e.g. to cm) to enable meaningful behavioral quantification.

#### Functionality
The Transform_DLC repository takes care of a specific task: It takes DeepLabCut dataframes as the input and outputs transformed and scaled DeepLabCut dataframes. Requirements for this transformation and scaling are that the behavioral maze or a reference has to be rectangular and its corners have to be tracked with DeepLabCut.

#### Usage
For an example usecase check out the tutorial notebook!

1) Set hyperparameter in config file: Specify the name of the horizontal and vertical basis vector markers (in a rectangular maze these are two opposing corners) and the origin (the corner that connects the two basis vector corners). Additionally, set the DeepLabCut-likelihood threshold for those markers, and the scale factors (optional, if you don´t need scaling set them to 1). For quality control set show_angle to True.

2) Instantiate the DLCTransformer class with the filepath to your DeepLabCut tracked data and the config-filepath.

3) Use .run on your instantiated class object and save the output in a variable of your choice.


#### Contribution
This is a [Defense Circuits Lab](https://www.defense-circuits-lab.com/) project written by [Michael Schellenberger](https://github.com/MSchellenberger) for [DLCutils](https://github.com/DeepLabCut/DLCutils).
<table>
<td>
    <a href="https://www.defense-circuits-lab.com/"> 
        <img src="https://static.wixstatic.com/media/547baf_87ffe507a5004e29925dbeb65fe110bb~mv2.png/v1/fill/w_406,h_246,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/LabLogo3black.png" alt="DefenseCircuitsLab" style="width: 250px;"/>
    </a>
</td>

</table>