from __future__ import annotations

from sklearn.model_selection import train_test_split

from training.dataset.dataset_builder import DatasetBuilder
from training.labeler import FutureLabeler
from training.features.feature_pipeline import FeaturePipeline

from training.evaluator import Evaluator
from training.model_registry import ModelRegistry
from training.experiment_tracker import ExperimentTracker
from training.early_stopping import EarlyStopping

from ai.models.model_manager import ModelManager

from training.sequence_builder import SequenceBuilder
from ai.models.data_loader import SequenceDataLoader
from training.validation.walk_forward import WalkForwardValidation


class Trainer:
    """
    Main AI Training Pipeline

    Pipeline

    Historical Data
            ↓
    Dataset Builder
            ↓
    Label Generator
            ↓
    Feature Pipeline
            ↓
    Train / Validation Split
            ↓
    Sequence Builder
            ↓
    LightGBM + LSTM
            ↓
    Evaluation
            ↓
    Save Models
    """

    def __init__(self):

        self.dataset_builder = DatasetBuilder()

        self.labeler = FutureLabeler()

        self.feature_pipeline = FeaturePipeline()

        self.evaluator = Evaluator()

        self.registry = ModelRegistry()

        self.tracker = ExperimentTracker()

        self.early_stopping = EarlyStopping()

        self.models = ModelManager()

        self.sequence_builder = SequenceBuilder()

        self.sequence_loader = SequenceDataLoader()

        self.walk_forward = WalkForwardValidation()


    ###############################################################

    def prepare_dataset(
        self,
        feature_dataframe,
    ):

        self.dataset_builder.add_features(
            feature_dataframe
        )

        dataset = self.dataset_builder.build()

        dataset = self.labeler.generate(
            dataset
        )

        dataset = self.feature_pipeline.process(
            dataset
        )

        return dataset


        def train_walk_forward(

    self,

    dataframe,

):

    return self.walk_forward.run(

        dataframe,

        self,

    )

    ###############################################################

    def split(
        self,
        dataset,
        test_size=0.20,
    ):

        x = dataset.drop(
            columns=["label"]
        )

        y = dataset["label"]

        return train_test_split(
            x,
            y,
            test_size=test_size,
            shuffle=False,
        )

    ###############################################################

    def train(
        self,
        feature_dataframe,
        model_name="primary_model",
    ):

        ###########################################################

        dataset = self.prepare_dataset(
            feature_dataframe
        )

        ###########################################################

        (
            x_train,
            x_validation,
            y_train,
            y_validation,
        ) = self.split(
            dataset
        )

        ###########################################################
        # Sequence Dataset
        ###########################################################

        x_seq, y_seq = self.sequence_builder.create(

            x_train.values,

            y_train.values,

        )

        sequence_loader = self.sequence_loader.build(

            x_seq,

            y_seq,

        )

        ###########################################################
        # Train All Models
        ###########################################################

        self.models.train(

            x_train,

            y_train,

            sequence_loader,

        )

        ###########################################################
        # Ensemble Prediction
        ###########################################################

        predictions = self.models.predict(

            x_validation,

        )

        ###########################################################

        metrics = self.evaluator.evaluate(

            y_validation,

            predictions,

        )

        ###########################################################

        self.tracker.log(

            metrics

        )

        ###########################################################

        stop = self.early_stopping.update(

            metrics["accuracy"]

        )

        ###########################################################
        # Save Every Model
        ###########################################################

        for name, model in self.models.models.items():

            self.registry.save(

                model,

                f"{model_name}_{name}",

            )

        ###########################################################

        return {

            "metrics": metrics,

            "samples": len(dataset),

            "early_stop": stop,

        }