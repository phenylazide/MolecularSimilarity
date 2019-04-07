#!/usr/bin/env python3
""""
Division of pairs to files based on AUC, EF 1%, EF 5%. We have some baseline model and
if our pair has better results(means > ) e.g. in AUC and EF 5% then we add this pair to file aucef5.
So outputfiles are:
auc, aucef1, aucaf5, aucef1ef5, ef1, ef1ef5, ef5
"""
import argparse
import json

import inputoutput_utils


def _main():
    configuration = _read_configuration()
    active_indexes = []
    with open(configuration["input_fragments"]) as input_stream:
        for new_line in input_stream:
            line = json.loads(new_line)
            for fragment in line["fragments"]:
                if fragment["index"] not in active_indexes:
                    active_indexes.append(fragment["index"])
    pairs = []
    for i in range(len(active_indexes)-1):
        for j in range(i+1, len(active_indexes)):
            pairs.append([active_indexes[i], active_indexes[j]])
    auc = 0
    ef1 = 0
    ef5 = 0
    with open(configuration["baseline_output"], "r", encoding="utf-8") as input_stream:
        for new_line in input_stream:
            line = json.loads(new_line)
            auc = line["AUC"]
            ef1 = line["EF1"]
            ef5 = line["EF5"]

    inputoutput_utils.create_parent_directory(configuration["output_directory"] + "/0")
    _prepare_files(configuration["output_directory"])
    for i in range(25651):
        with open(configuration["input_directory"] + "/evaluation" + str(i) + ".json",
                  "r", encoding="utf-8") as input_stream:
            for new_line in input_stream:
                line = json.loads(new_line)
                output = {
                    "pair": pairs[i]
                }
                if (line["AUC"] > auc) and (line["EF1"] > ef1) and(line["EF5"] > ef5):
                    with open(configuration["output_directory"] + "/aucef1ef5.json",
                              "a", encoding="utf-8") as output_stream:
                        json.dump(output, output_stream)
                        output_stream.write("\n")
                elif (line["AUC"] > auc) and (line["EF1"] > ef1):
                    with open(configuration["output_directory"] + "/aucef1.json",
                              "a", encoding="utf-8") as output_stream:
                        json.dump(output, output_stream)
                        output_stream.write("\n")
                elif (line["AUC"] > auc) and (line["EF5"] > ef5):
                    with open(configuration["output_directory"] + "/aucef5.json",
                              "a", encoding="utf-8") as output_stream:
                        json.dump(output, output_stream)
                        output_stream.write("\n")
                elif (line["EF1"] > ef1) and (line["EF5"] > ef5):
                    with open(configuration["output_directory"] + "/ef1ef5.json",
                              "a", encoding="utf-8") as output_stream:
                        json.dump(output, output_stream)
                        output_stream.write("\n")
                elif line["AUC"] > auc:
                    with open(configuration["output_directory"] + "/auc.json",
                              "a", encoding="utf-8") as output_stream:
                        json.dump(output, output_stream)
                        output_stream.write("\n")
                elif line["EF5"] > ef5:
                    with open(configuration["output_directory"] + "/ef5.json",
                              "a", encoding="utf-8") as output_stream:
                        json.dump(output, output_stream)
                        output_stream.write("\n")
                elif line["EF1"] > ef1:
                    with open(configuration["output_directory"] + "/ef1.json",
                              "a", encoding="utf-8") as output_stream:
                        json.dump(output, output_stream)
                        output_stream.write("\n")


def _prepare_files(output_directory: str):
    with open(output_directory + "/aucef1ef5.json",
              "w", encoding="utf-8"):
        pass
    with open(output_directory + "/aucef1.json",
              "w", encoding="utf-8"):
        pass
    with open(output_directory + "/aucef5.json",
              "w", encoding="utf-8"):
        pass
    with open(output_directory + "/ef1ef5.json",
              "w", encoding="utf-8"):
        pass
    with open(output_directory + "/auc.json",
              "w", encoding="utf-8"):
        pass
    with open(output_directory + "/ef1.json",
              "w", encoding="utf-8"):
        pass
    with open(output_directory + "/ef5.json",
              "w", encoding="utf-8"):
        pass


def _read_configuration() -> dict:
    parser = argparse.ArgumentParser(description="analysis of a lot of results")
    parser.add_argument("-f", type=str, dest="input_fragments", required=True)
    parser.add_argument("-b", type=str, dest="baseline_output", required=True)
    parser.add_argument("-d", type=str, dest="input_directory", required=True)
    parser.add_argument("-o", type=str, dest="output_directory",
                        help="output json lines file", required=True)
    return vars(parser.parse_args())


if __name__  == "__main__":
    _main()

