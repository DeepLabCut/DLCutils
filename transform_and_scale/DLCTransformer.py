import pandas as pd
import numpy as np
from read_config import read_config
from typing import Optional

class DLCTransformer:
    def __init__(self, config_filepath: str, dlc_filepath: Optional[str] = None, dlc_df: Optional[pd.DataFrame] = None):
        self.config = read_config(config_filepath)
        self.dlc_filepath = dlc_filepath
        if self.dlc_filepath is not None:
            if self.dlc_filepath.endswith("h5"):
                self.dlc_df = pd.read_hdf(dlc_filepath, header=[0, 1, 2], index_col=0)
            elif self.dlc_filepath.endswith("csv"):
                self.dlc_df = pd.read_csv(dlc_filepath, header=[0, 1, 2], index_col=0)
            else:
                raise ValueError("DeepLabCut file must be .h5 or .csv")
        else:
            if dlc_df is not None:
                self.dlc_df = dlc_df
            else:
                raise ValueError("One of the arguments dlc_filepath or dlc_df must be specified")

        # read metadata
        self.origin_marker = self.config["origin_marker"]
        self.basis_vector_h_marker = self.config["basis_vector_h_marker"]
        self.basis_vector_v_marker = self.config["basis_vector_v_marker"]
        self.scale_factor_h = self.config["scale_factor_h"]
        self.scale_factor_v = self.config["scale_factor_v"]
        self.dlc_immobile_marker_threshold = self.config[
            "dlc_immobile_marker_threshold"
        ]
        self.show_angle = self.config["show_angle"]
        self.scorer = self.dlc_df.columns.get_level_values(0).unique()[0]

    def run(self) -> pd.DataFrame:
        """
        Translate and scale DLC data.
        First get median coordinate of origin marker and basis vectors, then transform and scale the data.

        :return: pd.DataFrame with transformed and scaled DLC data
        """
        # get basis vectors and origin
        origin, basis_vector_h, basis_vector_v = self.get_basis_vectors(
            df=self.dlc_df,
            origin_marker=self.origin_marker,
            basis_vector_h_marker=self.basis_vector_h_marker,
            basis_vector_v_marker=self.basis_vector_v_marker,
            dlc_immobile_marker_threshold=self.dlc_immobile_marker_threshold,
        )

        if self.show_angle:
            print(
                "Angle between basis vectors :",
                self._calculate_angle(basis_vector_v, (0, 0), basis_vector_h),
            )

        # transform df
        df_transformed = self.transform(
            self.dlc_df, origin, basis_vector_h, basis_vector_v
        )
        df_scaled = self.scale_df(
            df_transformed, self.scale_factor_h, self.scale_factor_v
        )
        return df_scaled

    def get_basis_vectors(
        self,
        df: pd.DataFrame,
        origin_marker: str,
        basis_vector_h_marker: str,
        basis_vector_v_marker: str,
        dlc_immobile_marker_threshold: float,
    ) -> (tuple, tuple, tuple):
        """
        Returns the origin and basis vectors of the coordinate system

        :param df: pd.DataFrame with tracking data
        :param origin_marker: name of origin marker
        :param basis_vector_h_marker: name of horizontal basis vector marker
        :param basis_vector_v_marker: name of vertical basis vector marker
        :param dlc_immobile_marker_threshold: minimum likelihood of a constant marker to be included into the median coordinate calculation
        :return: coordinates of origin, basis_vector_h, basis_vector_v
        """
        origin = self.get_median_coordinate(
            df, origin_marker, dlc_immobile_marker_threshold
        )

        # bring coordinates into origin system
        basis_vector_h_coord = self.get_median_coordinate(
            df=df,
            marker=basis_vector_h_marker,
            dlc_immobile_marker_threshold=dlc_immobile_marker_threshold,
        )
        basis_vector_v_coord = self.get_median_coordinate(
            df=df,
            marker=basis_vector_v_marker,
            dlc_immobile_marker_threshold=dlc_immobile_marker_threshold,
        )

        # calculate basis vector transformation
        basis_vector_h = (
            basis_vector_h_coord[0] - origin[0],
            basis_vector_h_coord[1] - origin[1],
        )
        basis_vector_v = (
            basis_vector_v_coord[0] - origin[0],
            basis_vector_v_coord[1] - origin[1],
        )

        return origin, basis_vector_h, basis_vector_v

    def get_median_coordinate(self, df, marker, dlc_immobile_marker_threshold) -> tuple:
        """
        Returns the most likely coordinate of a vector

        :param df: pd.DataFrame with tracking data
        :param marker: name of marker of which the median coordinate should be calculated
        :param dlc_immobile_marker_threshold: minimum likelihood of a constant marker to be included into the median coordinate calculation
        :return: median coordinate of marker
        """
        # filter df
        df = df.droplevel(0, axis=1)
        marker_df = df.loc[
            df[marker, "likelihood"] > dlc_immobile_marker_threshold, marker
        ].copy()
        x_coord = np.nanmedian(marker_df["x"])
        y_coord = np.nanmedian(marker_df["y"])
        coords = (x_coord, y_coord)
        return coords

    def _calculate_angle(self, a, b, c) -> float:
        """
        Calculates the angle between three points a-b-c

        :param a: tuple of coordinates
        :param b: tuple of coordinates
        :param c: tuple of coordinates
        :return: angle between a-b-c in degrees
        """

        # Calculate the vectors AB and BC
        vector_AB = (b[0] - a[0], b[1] - a[1])
        vector_BC = (c[0] - b[0], c[1] - b[1])

        # Calculate the magnitudes of AB and BC
        magnitude_AB = np.linalg.norm(vector_AB)
        magnitude_BC = np.linalg.norm(vector_BC)
        #
        # Calculate the dot product of AB and BC
        dot_product = np.dot(vector_AB, vector_BC)

        # Calculate the angle in radians using the dot product and magnitudes
        angle_radians = np.arccos(dot_product / (magnitude_AB * magnitude_BC))

        # Convert the angle to degrees
        angle_degrees = np.degrees(angle_radians)
        return angle_degrees

    def transform(self, df, origin, basis_vector_h, basis_vector_v) -> pd.DataFrame:
        """
        Transform the coordinates of the df into the new coordinate system

        :param df: pd.DataFrame with tracking data
        :param origin: coordinate of origin
        :param basis_vector_h: coordinate of horizontal basis vector
        :param basis_vector_v: coordinate of vertical basis vector
        :return: transformed pd.DataFrame
        """
        transformed_df = df.copy()
        final_transformed_df = df.copy()

        # 2d rotation matrix
        a = basis_vector_h[0]
        b = basis_vector_h[1]
        c = basis_vector_v[0]
        d = basis_vector_v[1]

        for marker in df.columns.get_level_values(1).unique():

            # shift coordinates into origin system
            transformed_df.loc[:, (self.scorer, marker, "x")] -= origin[0]
            transformed_df.loc[:, (self.scorer, marker, "y")] -= origin[1]

            # linear algebra 2D transformation
            final_transformed_df.loc[:, (self.scorer, marker, "y")] = (
                (transformed_df.loc[:, (self.scorer, marker, "y")] / b)
                - (transformed_df.loc[:, (self.scorer, marker, "x")] / a)
            ) / ((-c / a) + (d / b))

            final_transformed_df.loc[:, (self.scorer, marker, "x")] = (
                transformed_df.loc[:, (self.scorer, marker, "x")]
                - c * final_transformed_df.loc[:, (self.scorer, marker, "y")]
            ) / a

        return final_transformed_df

    def scale_df(self, df, scale_factor_h, scale_factor_v) -> pd.DataFrame:
        """
        :param df: pd.DataFrame with tracking data
        :param scale_factor_h: horizontal scale factor
        :param scale_factor_v: vertical scale factor
        :return: scaled pd.DataFrame
        """
        scaled_df = df.copy()
        for marker in df.columns.get_level_values(1).unique():
            scaled_df.loc[:, (self.scorer, marker, "x")] *= scale_factor_h
            scaled_df.loc[:, (self.scorer, marker, "y")] *= scale_factor_v
        return scaled_df
