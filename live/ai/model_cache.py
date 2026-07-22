from __future__ import annotations

from threading import Lock


class ModelCache:
    """
    Thread-safe singleton cache for live models.
    """

    _instance = None

    _lock = Lock()

    ###########################################################

    def __new__(cls):

        with cls._lock:

            if cls._instance is None:

                cls._instance = super().__new__(cls)

                cls._instance._model = None

                cls._instance._metadata = {}

        return cls._instance

    ###########################################################

    def set(

        self,

        model,

        **metadata,

    ):

        self._model = model

        self._metadata = metadata

    ###########################################################

    def get(self):

        return self._model

    ###########################################################

    def metadata(self):

        return dict(self._metadata)

    ###########################################################

    def loaded(self):

        return self._model is not None

    ###########################################################

    def clear(self):

        self._model = None

        self._metadata.clear()