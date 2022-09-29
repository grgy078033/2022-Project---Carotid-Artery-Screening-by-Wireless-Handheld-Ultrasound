import tensorflow as tf

## 將h5的model轉成tflite moddel

# 設定路徑 & 名稱
modelPath = './model0326_crop.h5'
tflitePath = './model0326_crop_Lite.tflite'

#載入model & 設定轉出大小
model = tf.saved_model.load(modelPath)
model.signatures[tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY].inputs[0].set_shape((2, 1, 128, 512, 1))
tf.saved_model.save(model, tflitePath, signatures=model.signatures[tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY])

# 轉換
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir=tflitePath, signature_keys=['serving_default'])
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS, tf.lite.OpsSet.SELECT_TF_OPS]
tflite_model = converter.convert()