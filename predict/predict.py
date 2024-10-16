from functools import partial
import argparse
import os


import numpy as np
import paddle
import paddle.nn.functional as F
import paddlenlp as ppnlp
from paddlenlp.datasets import load_dataset
from paddlenlp.data import Stack, Tuple, Pad
from paddlenlp.transformers import *

from data import create_dataloader, read_text_pair, convert_example
from ..train.post_gru import QuestionMatching

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", type=str, required=True, help="The full path of input file")
parser.add_argument("--result_file", type=str, required=True, help="The result file name")
parser.add_argument("--params_path", default='./work/user_data/gaiic_eda_real_pool_gru_droo0.4+0.2_checkpoints/model_17800_acc_0.8805/model_state.pdparams', help="The path to model parameters to be loaded.")
parser.add_argument("--max_seq_length", default=256, type=int,
                    help="The maximum total input sequence length after tokenization. "
                         "Sequences longer than this will be truncated, sequences shorter will be padded.")
parser.add_argument("--batch_size", default=32, type=int, help="Batch size per GPU/CPU for training.")
parser.add_argument('--device', choices=['cpu', 'gpu'], default="gpu",
                    help="Select which device to train model, defaults to gpu.")
args = parser.parse_args()

def predict(model, data_loader):
    """
    Predicts the data labels.
    Args:
        model (obj:`QuestionMatching`): A model to calculate whether the question pair is semantically similar or not.
        data_loader (obj:`List(Example)`): The processed data ids of text pair: [query_input_ids, query_token_type_ids, title_input_ids, title_token_type_ids]
    Returns:
        results(obj:`List`): cosine similarity of text pairs.
    """
    batch_logits = []

    model.eval()

    with paddle.no_grad():
        for batch_data in data_loader:
            input_ids, token_type_ids = batch_data

            input_ids = paddle.to_tensor(input_ids)
            token_type_ids = paddle.to_tensor(token_type_ids)

            batch_logit, _ = model(
                input_ids=input_ids, token_type_ids=token_type_ids)

            batch_logits.append(batch_logit.numpy())

        batch_logits = np.concatenate(batch_logits, axis=0)

        return batch_logits

if __name__ == "__main__":
    paddle.set_device(args.device)

    pretrained_model = ppnlp.transformers.ErnieGramModel.from_pretrained(
        'ernie-gram-zh')
    tokenizer = ppnlp.transformers.ErnieGramTokenizer.from_pretrained(
        'ernie-gram-zh')

    trans_func = partial(
        convert_example,
        tokenizer=tokenizer,
        max_seq_length=args.max_seq_length,
        is_test=True)

    batchify_fn = lambda samples, fn=Tuple(
        Pad(axis=0, pad_val=tokenizer.pad_token_id),  # input_ids
        Pad(axis=0, pad_val=tokenizer.pad_token_type_id),  # segment_ids
    ): [data for data in fn(samples)]

    test_ds = load_dataset(
        read_text_pair, data_path=args.input_file, is_test=True, lazy=False)

    test_data_loader = create_dataloader(
        test_ds,
        mode='predict',
        batch_size=args.batch_size,
        batchify_fn=batchify_fn,
        trans_fn=trans_func)

    model = QuestionMatching(pretrained_model)

    if args.params_path and os.path.isfile(args.params_path):
        state_dict = paddle.load(args.params_path)
        model.set_dict(state_dict)
        print("Loaded parameters from %s" % args.params_path)
    else:
        raise ValueError(
            "Please set --params_path with correct pretrained model file")

    y_probs = predict(model, test_data_loader)
    y_preds = np.argmax(y_probs, axis=1)

    with open(args.result_file, 'w', encoding="utf-8") as f:
        for y_pred in y_preds:
            f.write(str(y_pred) + "\n")