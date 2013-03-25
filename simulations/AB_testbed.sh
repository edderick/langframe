POINTS_PER_WORD=2
REPEATS=5
TRAINING_ITERATIONS=25
SAMPLES=1000
K=3 #unused

cd ..
rm simulations/logs/ab_*
rm simulations/logs/sample_*
rm simulations/logs/dist_*

for i in {1..5}
do

echo $i

visualisation/tests/random_source.R $POINTS_PER_WORD > simulations/logs/sample_$i
echo "done sample"

python -m simulations.train_ab simulations/logs/sample_$i -I $TRAINING_ITERATIONS -N $SAMPLES > simulations/logs/ab_$i
echo "done simulation"

cat simulations/logs/ab_$i | visualisation/language_distance.R $(visualisation/argsAB.py) > simulations/logs/dist_$i
echo "done distance"

cat simulations/logs/dist_$i | visualisation/iteration_graph.R graph_$i
echo "done graph"

done
