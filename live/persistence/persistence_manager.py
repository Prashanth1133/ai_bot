from __future__ import annotations

from pathlib import Path
import json


class PersistenceManager:

    def save(

        self,

        filename,

        data,

    ):

        path = Path(filename)

        path.parent.mkdir(

            parents=True,

            exist_ok=True,

        )

        with open(

            path,

            "w",

            encoding="utf-8",

        ) as fp:

            json.dump(

                data,

                fp,

                indent=4,

            )

    def load(

        self,

        filename,

    ):

        path = Path(filename)

        if not path.exists():

            return None

        with open(

            path,

            "r",

            encoding="utf-8",

        ) as fp:

            return json.load(fp)