POINTS_PER_WORD=2
REPEATS=1
TRAINING_ITERATIONS=500
SAMPLES=1000
SKIP=25
K=3 #unused

cd ..
rm simulations/logs/ab_*
rm simulations/logs/sample_*
rm simulations/logs/dist_*

for i in {1..5}
do

echo $i

visualisation/tests/random_source.R $POINTS_PER_WORD > simulations/logs/ab/sample_$i
echo "done sample"

python -m simulations.train_ab simulations/logs/ab/sample_$i -I $TRAINING_ITERATIONS -N $SAMPLES --skip $SKIP > simulations/logs/ab_$i
echo "done simulation"

cat simulations/logs/ab_$i | visualisation/language_distance.R $(visualisation/argsAB.py) > simulations/logs/ab/dist_$i
echo "done distance"

cat simulations/logs_ab/dist_$i | visualisation/iteration_graph.R graph_$i
echo "done graph"

done
