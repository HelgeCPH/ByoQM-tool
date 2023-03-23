from collections import defaultdict
import csv
from datetime import datetime
import importlib
import os
from pathlib import Path
import sys
import pandas as pd
from bokeh.layouts import gridplot
from bokeh.plotting import show
import logging


class Dashboard:
    def _check_data(self, in_use_qm, target_path, filename):
        file_location = "./output/metadata/" + filename
        df = pd.read_csv(file_location, skiprows=0)
        for row in df.itertuples(index=False, name=None):
            is_right_qm = self._check_qm(row[0], in_use_qm)
            is_right_src = self._check_src_root(row[1], target_path)
            if not is_right_qm or not is_right_src:
                return False

        return True

    def _check_src_root(self, targetSrc, actualSrc):
        if ("./" + targetSrc) != actualSrc:
            return False
        return True

    def _check_qm(self, targetQM, actualQM):
        if targetQM != actualQM:
            return False
        return True

    def _check_date(self, date, start_date, end_date):
        if start_date > date or end_date < date:
            return False
        return True

    def _get_files(self):
        figure_files = os.listdir("./figures")
        figure_files.remove("__pycache__")
        for file in figure_files:
            figure_files.remove(file)
            figure_files.append("./figures/" + file)
        return figure_files

    # Returns bokeh objects, for input in gridplot.
    def _get_figures(self, data):
        results = {}
        figures = self._get_files()
        for figure_file in figures:
            spec = importlib.util.spec_from_file_location("figure", figure_file)
            module = importlib.util.module_from_spec(spec)
            sys.modules["figure"] = module
            spec.loader.exec_module(module)
            module.fig._data = data
            results["figure"] = module.fig.get_figure()
        return results

    def show_graphs(
        self, in_use_qm: str, targetPath: Path, start_date: datetime, end_date: datetime
    ):
        """
        This method is used to display the graphs chosen. At the moment, only line graphs can be chosen,
        however this can be easily expanded upon.

        The method makes use of Bokeh to generate figures, which are then added to a gridplot in the
        arrangement of an arbitrary amount of rows where each row contains two figures.
        """
        data = self.get_data(in_use_qm, targetPath, start_date, end_date)
        # Need to get figure type in a dict, so that they can be passed to gridplot.
        # Format: {figure_type (str) : figure_objects (list)}
        figures = self._get_figures(data).get("figure")
        gridplots = gridplot(
            [[figures[i], figures[i + 1]] for i in range(0, len(figures) - 1, 2)],
        )
        show(gridplots)

    def get_data(
        self,
        in_use_qm: str,
        targetPath: Path,
        start_date: datetime,
        end_date: datetime,
        path="./output/frequencies",
    ):
        """
        Gets data from specified path. The path is defaulted to the output folder, but if you want to run
        BYOQM using a different path, this can be changed in the CLI.

        The name of the file depicts the date at which the tool was run. The content of the file consists
        of an arbitrary amount of metrics, together with their respective values.
        This data is collected in a dict, matching every single metric to a list containing
        tuples of dates and values.

        Graphs are only generated for the current chosen quality model and the current target path.

        The data is then sorted to ensure that the dates appear in chronological order
        """
        logging.info(f"Getting data from: {path}")
        graph_data = defaultdict(list)
        for filename in os.listdir(path):
            try:
                filepath = os.path.join(path, filename)
                date = datetime.strptime(filename.split(".")[0], "%Y-%m-%d_%H-%M-%S")

                if not self._check_date(date, start_date, end_date):
                    continue
                if not self._check_data(in_use_qm, targetPath, filename):
                    continue

                df = pd.read_csv(filepath, skiprows=0)
                for row in df.itertuples(index=False, name=None):
                    graph_data[row[0]].append((date, row[1]))
            except:
                logging.warning(
                    f"Failed to parse file with filename: {filename} - invalid format. Check the naming convention of the file or the content of the file"
                )
        for key, v in graph_data.items():
            try:
                v.sort()
            except:
                logging.warning(f"Failed to sort data for {key} in graph_data")
        logging.info("Finished getting data")
        return graph_data