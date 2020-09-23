"""
Nelly Kane
10.18.2019

TargetTracker.py
"""
import numpy as np
from pandas import DataFrame

from location import ItemLocation, CameraData
from position_predict import ItemLocationModel
from util import munkres


########################################################################################################################
class TrackData:
    """
    A class to hold track data, current or final, and the appropriate methods to set, retrieve and operate on that track
    data.
    """
    TRACK_ID_STRING = 'trackID'
    OBJECT_DATA_STRING = 'ObjectData'
    COLUMNS = [TRACK_ID_STRING, OBJECT_DATA_STRING]

    ####################################################################################################################
    def __init__(self, name: str):
        """
        Constructor
            maximumTracks : maximum number of current tracks that can be stored at a given time. 
        """
        self.__name = name
        self.__trackDataFrame = DataFrame(columns=TrackData.COLUMNS)

    ####################################################################################################################
    def get_ids(self) -> list:
        """
        Method to return current track ID's 
        """
        return self.__trackDataFrame[TrackData.TRACK_ID_STRING].values.tolist()

    ####################################################################################################################
    def remove_by_id(self, id_int: int) -> ItemLocation:
        """
        Method to remove a track by ID and return it.
        """
        dfIndex = self.__trackDataFrame.index[self.__trackDataFrame[TrackData.TRACK_ID_STRING] == id_int].values[0]
        objectLocation = self.__trackDataFrame.at[dfIndex, TrackData.OBJECT_DATA_STRING]

        self.__trackDataFrame = self.__trackDataFrame.drop(dfIndex)

        return objectLocation

    ####################################################################################################################
    def add_track(self, objectLocation: ItemLocation) -> None:
        """
        A method to append a new track by ID.
        """
        self.__trackDataFrame = self.__trackDataFrame.append({TrackData.TRACK_ID_STRING: objectLocation.getObjectID(),
                                                              TrackData.OBJECT_DATA_STRING: objectLocation},
                                                             ignore_index=True)

        return

    ####################################################################################################################
    def append_to_data_by_id(self, iD: int, cameraData: CameraData, pixel: list) -> None:
        """
        A method to append to a current track by ID.
        """
        dfIndex = self.__trackDataFrame.index[self.__trackDataFrame[TrackData.TRACK_ID_STRING] == iD].values[0]
        objectLocation = self.__trackDataFrame.at[dfIndex, TrackData.OBJECT_DATA_STRING]

        objectLocation.addNewObservation(cameraData=cameraData, pixel=pixel)

        return

    ####################################################################################################################
    def get_data_by_id(self, iD: int) -> ItemLocation:
        """
        Method for returning ObjectLocation data by ID.
        """
        dfIndex = self.__trackDataFrame.index[self.__trackDataFrame[TrackData.TRACK_ID_STRING] == iD].values[0]
        return self.__trackDataFrame.at[dfIndex, TrackData.OBJECT_DATA_STRING]

    ####################################################################################################################
    def get_id_by_index(self, index: int) -> int:
        """
        Method for returning the ID stored at a given index.
        """
        return self.__trackDataFrame.at[index, TrackData.TRACK_ID_STRING]

    ####################################################################################################################
    def print_data(self) -> None:
        """
        Method to print print track data to the console.
        """
        for index, row in self.__trackDataFrame.iterrows():
            print(' //////////////////// DATA PRINT FOR TRACK : ' + str(row[TrackData.TRACK_ID_STRING]) + ' //////////')
            print(TrackData.OBJECT_DATA_STRING + ':')
            row[TrackData.OBJECT_DATA_STRING].printResults()

        return

    ####################################################################################################################
    def get_data(self) -> DataFrame:
        """
        A method to return the underlying track dataframe.
        """
        return self.__trackDataFrame

    ####################################################################################################################
    def get_name(self) -> str:
        """
        Method to return string name.
        """
        return self.__name

    ####################################################################################################################
    def get_size(self) -> int:
        """
        Method to return the current size of the underlying dataframe.
        """
        return len(self.__trackDataFrame)


########################################################################################################################
class TargetTracker:
    """
    A class to compute object-to-object associations between frames with knowledge of sensor location/orientation 
    metadata and a predictive model approximating where an object might appear in a future frame given a current frame.
    """
    # static variables
    MAX_OBSERVATIONS = 10
    MAX_CURRENT_TRACKS = 10
    MAX_FINAL_TRACKS = 100
    LARGE_VAL = np.inf
    SMALL_VAL = 1 / LARGE_VAL

    # instantiate the assignment backend
    assignmentAlgorithm = munkres.Munkres()

    ####################################################################################################################
    def __init__(self, gateSize: int, distToDVec: float):
        """
        Constructor
            gateSize: circular gate size used by the cost matrix to compute possible associations
            distToDVec: shortest distance from object to direction vector (vector in 3D space from camera pos t to t+1) 
        """
        self.gateSize = gateSize  # size of gate in pixels

        # instantiate the object motion model
        self.objectMotion = ItemLocationModel(W=distToDVec)

        # start Pandas.DataFrames
        self.__currentTrackDataFrame = TrackData(name='CURRENT_TRACKS')
        self.__finalTrackDataFrame = TrackData(name='FINAL TRACKS')

    ####################################################################################################################
    def add_frame_observations(self, observations: list, curCameraData: CameraData) -> None:
        """
        This function passes in a list of 'observations' as pixels [row, col] and a current CameraData instance 
        associated with them. It attempts to associate the new observations with tracks. For those observations that an 
        association is not made, new object instances will begin.
            observations: list of [row, col]  lists representing objects
            curCameraData: CameraData instance associated with observations
        """
        # grab size of current __currentTrackDataFrame
        numCurrentTracks = self.__currentTrackDataFrame.get_size()

        # Get track ID's. NOTE: This is a list. trackIDs
        trackIDs = self.__currentTrackDataFrame.get_ids()

        # NOTE: This will be used to remove unused tracks at the end. As tracks are used they will be
        # removed from this list, and the remaining list will be removed from the current track list.
        trackIDsUnused = trackIDs.copy()

        # make a prediction for each current track, NOTE: the loop doesn't execute if numCurrentTracks = 0
        predictions = self.__build_predictions(trackIDs=trackIDs, newCameraData=curCameraData)

        # build cost matrix with observations and predictions
        costMatrix = self.build_cost_matrix(observations, predictions)

        # run the association backend on the cost matrix
        costSolnIndices = TargetTracker.assignmentAlgorithm.compute(costMatrix)

        # loop over cost matrix solution indices
        for costSolution in costSolnIndices:

            obsIdx = costSolution[0]
            predIdx = costSolution[1]

            if (predIdx) < numCurrentTracks:  # append data to old track
                # get track ID the current observation will append to
                trackID = self.__currentTrackDataFrame.get_id_by_index(predIdx)
                # append observation data to current track
                self.__currentTrackDataFrame.append_to_data_by_id(iD=trackID, cameraData=curCameraData,
                                                                  pixel=observations[obsIdx])
                # remove used track from unused list
                trackIDsUnused.remove(trackID)

            else:  # begin new track
                # create new object location object
                objectLocation = ItemLocation(origCameraData=curCameraData, origPixel=observations[obsIdx])
                # create new track
                self.__currentTrackDataFrame.add_track(objectLocation=objectLocation)

        # remove tracks that were NOT updated from the track list and add them to final tracks
        for dropID in trackIDsUnused:
            objectForMove = self.__currentTrackDataFrame.remove_by_id(dropID)
            self.__finalTrackDataFrame.add_track(objectForMove)

        return

    ####################################################################################################################
    def print_current_track_results(self) -> None:
        """
        A method to print track results that are current and still available for aditional data append.
        """
        self.__currentTrackDataFrame.print_data()

        return

    ####################################################################################################################
    def print_final_track_results(self) -> None:
        """
        A method to print track results that are current and still available for aditional data append.
        """
        self.__finalTrackDataFrame.print_data()

        return

    ####################################################################################################################
    def __build_predictions(self, trackIDs: list, newCameraData: CameraData) -> list:
        """
        Method for computing predictions of current tracks with camera data.
        """
        predictions = []
        for trackID in trackIDs:
            trkObject = self.__currentTrackDataFrame.get_data_by_id(trackID)
            trkCameraData = trkObject.getRecentCameraData()
            trkPixel = trkObject.getRecentPixel()

            predictedPixel = self.objectMotion.itemLocationPredictor(objRowCol=trkPixel,
                                                                     camData1=trkCameraData, camData2=newCameraData)

            predictions.append(predictedPixel)

        return predictions

    ####################################################################################################################
    def build_cost_matrix(self, observations: list, predictions: list, printMatrix: bool = False) -> np.array:
        """
        construction of the cost matrix as a numpy array. Size: [number obs, number obs + num current tracks]
        """
        numObservations = len(observations)
        numTracks = len(predictions)

        # value of perfect overlap, zero distance between obs and track
        bestMatch = np.pi * self.gateSize ** 2

        costMatrix = np.zeros((numObservations, numObservations + numTracks), dtype=float)

        # input will both be two dimensional lists
        for obsIdx in np.arange(numObservations):
            for trkIdx in np.arange(numTracks):
                curObs = observations[obsIdx]  # should be a len 2 list here
                curTrk = predictions[trkIdx]  # should be a len 2 list here

                # value of overlapping gates
                matchVal = self.gate(prediction=curTrk, observation=curObs)

                # TODO revisit this
                if (matchVal == 0):
                    costVal = np.inf
                else:
                    costVal = bestMatch - matchVal  # note: if match = best, cost = 0
                costMatrix[obsIdx, trkIdx] = costVal

        # build right side of array
        for obsIdx in np.arange(numObservations):
            for obsIdx2 in np.arange(numTracks, numTracks + numObservations):
                if (obsIdx == (obsIdx2 - numTracks)):
                    costMatrix[obsIdx, obsIdx2] = bestMatch
                else:
                    costMatrix[obsIdx, obsIdx2] = TargetTracker.LARGE_VAL

        if (printMatrix is True):
            TargetTracker.print_array(costMatrix)

        return costMatrix

    ####################################################################################################################
    def gate(self, prediction: list, observation: list) -> float:
        """
        compute gate for given prediction and observation. A gate is considered to be the overlap of two circles of
        radius 'gateSize' centered at prediction and observation respectively. The more accurate the model used for 
        predictions the tighter the game size can be. If there is no overlap then no association can be made and this
        returns a 0 (meaning a new track has to start itself)
            prediction: [row, col] list
            observation: [row, col] list
        """
        rowPred = prediction[0]
        colPred = prediction[1]
        rowObs = observation[0]
        colObs = observation[1]

        # calculate distance from prediction to observation
        dist = np.sqrt((rowPred - rowObs) ** 2 + (colPred - colObs) ** 2)

        if (dist >= 2 * self.gateSize):
            return 0
        else:
            # equation taken from 'http://mathworld.wolfram.com/Circle-CircleIntersection.html'
            R = self.gateSize
            A = 2 * R ** 2 * np.arccos(dist / (2 * R)) - (1.0 / 2.0) * np.sqrt(
                (dist ** 2) * (2 * R - dist) * (2 * R + dist))
            return A

    ####################################################################################################################
    def print_array(array: np.ndarray):
        """
        Static method to print cost matrix.
        """
        np.set_printoptions(precision=3)
        print(array)

        return
