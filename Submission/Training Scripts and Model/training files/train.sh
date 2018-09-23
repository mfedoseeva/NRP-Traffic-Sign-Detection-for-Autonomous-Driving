OBJ_DETECTION=/home/nfan/github/models/research
PIPELINE_CONFIG_PATH=./ssdlite_mobilenet_v2_coco.config
MODEL_DIR=./models/train
NUM_TRAIN_STEPS=82800
NUM_EVAL_STEPS=720
python $OBJ_DETECTION/object_detection/model_main.py \
    --pipeline_config_path=${PIPELINE_CONFIG_PATH} \
    --model_dir=${MODEL_DIR} \
    --num_train_steps=${NUM_TRAIN_STEPS} \
    --num_eval_steps=${NUM_EVAL_STEPS} \
    --alsologtostderr
