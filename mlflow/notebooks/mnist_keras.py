from PIL import Image
import tensorflow_datasets as tfds
import tensorflow as tf
import json
import numpy as np

def infer():
    (ds_train, ds_test), ds_info = tfds.load(
        'mnist',
        split=['train', 'test'],
        shuffle_files=True,
        as_supervised=True,
        with_info=True,
    )

    def normalize_img(image, label):
        """Normalizes images: `uint8` -> `float32`."""
        print(image)

        # out = tf.identity(image)
        #
        # sess =  tf.compat.v1.Session()
        # print(sess.run(out))
        #
        # out = sess.run(out)
        #
        # img = Image.fromarray(out.numpy())
        # img.show()
        # img.save("digit__{}.jpg".format(label))


        return tf.cast(image, tf.float32) / 255., label


    ds_test = ds_test.map(
        normalize_img, num_parallel_calls=tf.data.experimental.AUTOTUNE)
    ds_test = ds_test.batch(128)
    ds_test = ds_test.cache()
    ds_test = ds_test.prefetch(tf.data.experimental.AUTOTUNE)


    model = tf.saved_model.load("/BIG_FILES/mnist-keras")

    infer = model.signatures["serving_default"]
    print("input format", infer.structured_input_signature)
    print("output format", infer.structured_outputs)

    input_ = list(ds_test)[0][0].numpy().reshape(128, 28, 28)[:1]



    label = list(ds_test)[0][1].numpy().tolist()[:1]

    in1 = input_[0]*255
    in2 = in1.astype(np.uint8)
    img = Image.fromarray(in2)
    img.show()
    #img.save("digit_{}.jpg".format(label[0]))

    res = infer(tf.constant(input_))

    print("input", input_.tolist())
    print("logit", res["dense_1"].numpy())
    predict = res["dense_1"].numpy().argmax(1).tolist()

    sample_input = {"signature_name": "serving_default", "instances": input_.tolist()}

    with open("sample_input.json", "w") as fp:
        json.dump(sample_input, fp)


    print(predict, label)

if __name__ == "__main__":
    pass
    #load_dataset("cifar10data")
    infer()