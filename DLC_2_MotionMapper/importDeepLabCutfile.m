function [bodypart1, bodypart2, bodypart3, bodypart4, bodypart5, bodypart6, bodypart7, bodypart8, bodypart9, bodypart10, bodypart11]= importDeepLabCutfile(filename, startRow, endRow)
%IMPORTFILE Import numeric data from a text file as column vectors.
%   [bodypart1, bodypart2, bodypart3, bodypart4, bodypart5, bodypart6]
%   = IMPORTFILE(FILENAME) Reads data from text file FILENAME for the
%   default selection.
%
%   [bodypart1, bodypart2, bodypart3, bodypart4, bodypart5, bodypart6]
%   = IMPORTFILE(FILENAME, STARTROW, ENDROW) Reads data from rows STARTROW
%   through ENDROW of text file FILENAME.
%
% Example:
%   [bodypart1, bodypart2, bodypart3, bodypart4, bodypart5, bodypart6]
%   =
%   importfile('yourdeeplabcutoutput_DeepCut_resnet50_ReachDec10shuffle1_1030000.csv',4, 1169);
%

%% Initialize variables.
delimiter = ',';
if nargin<=2
    startRow = 4;
    endRow = inf;
end

%% Format string for each line of text

% For more information, see the TEXTSCAN documentation.
formatSpec = '%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%[^\n\r]';

%% Open the text file.
fileID = fopen(filename,'r');

%% Read columns of data according to format string.
% This call is based on the structure of the file used to generate this
% code. If an error occurs for a different file, try regenerating the code
% from the Import Tool.
dataArray = textscan(fileID, formatSpec, endRow(1)-startRow(1)+1, 'Delimiter', delimiter, 'HeaderLines', startRow(1)-1, 'ReturnOnError', false);
for block=2:length(startRow)
    frewind(fileID);
    dataArrayBlock = textscan(fileID, formatSpec, endRow(block)-startRow(block)+1, 'Delimiter', delimiter, 'HeaderLines', startRow(block)-1, 'ReturnOnError', false);
    for col=1:length(dataArray)
        dataArray{col} = [dataArray{col};dataArrayBlock{col}];
    end
end

%% Close the text file.
fclose(fileID);

%% Post processing for unimportable data.
% No unimportable data rules were applied during the import, so no post
% processing code is included. To generate code which works for
% unimportable data, select unimportable cells in a file and regenerate the
% script.

%% Allocate imported array to column variable names
bodypart1 = dataArray{:, 1};
bodypart2 = dataArray{:, 2};
bodypart3 = dataArray{:, 3};
bodypart4 = dataArray{:, 4};
bodypart5 = dataArray{:, 5};
bodypart6 = dataArray{:, 6};
bodypart7 = dataArray{:, 7};
bodypart8 = dataArray{:, 8};
bodypart9 = dataArray{:, 9};
bodypart10 = dataArray{:, 10};
bodypart11 = dataArray{:, 11};

