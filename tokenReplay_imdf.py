from pm4py.algo.imdf.inductMinDirFollows import InductMinDirFollows as InductMinDirFollows
from pm4py.log.importer import xes as xes_importer
from pm4py.models.petri import visualize as pn_viz
from pm4py.algo.alignments import state_equation_classic
from pm4py.models import petri
from pm4py.algo.tokenreplay import token_replay
import time

log = xes_importer.import_from_path_xes('C:\\receipt.xes')
#log = xes_importer.import_from_path_xes('a32f0n00.xes')
imdf = InductMinDirFollows()
net, marking = imdf.apply(log)
for place in marking:
	print("initial marking "+place.name)
final_marking = petri.net.Marking()
for p in net.places:
    if not p.out_arcs:
        final_marking[p] = 1
for place in final_marking:
	print("final marking "+place.name)
gviz = pn_viz.graphviz_visualization(net)
gviz.view()
log = log[0:min(100,len(log))]
time0 = time.time()
print("started token replay")
[traceIsFit, traceFitnessValue, activatedTransitions, placeFitness] = token_replay.apply_log(log, net, marking, final_marking, enable_placeFitness=True)
for place in placeFitness:
	if len(placeFitness[place]['underfedTraces']) > 0:
		print(place.name)
print("underfed places: ",[place.name for place in placeFitness.keys() if len(placeFitness[place]['underfedTraces']) > 0])
print("overfed places: ",[place.name for place in placeFitness.keys() if len(placeFitness[place]['overfedTraces']) > 0])

time1 = time.time()
print("time interlapsed",(time1-time0))
fitTraces = [x for x in traceIsFit if x]
fitness = float(len(fitTraces))/float(len(log))
print("fitness = "+str(fitness))