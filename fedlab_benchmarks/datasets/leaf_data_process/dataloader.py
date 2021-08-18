# Copyright 2021 Peng Cheng Laboratory (http://www.szpclab.com/) and FedLab Authors (smilelab.group)

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
    get dataloader for dataset in LEAF processed
"""

import torch
import pickle
from .nlp_utils.vocab import Vocab
from .dataset.femnist_dataset import FemnistDataset
from .dataset.shakespeare_dataset import ShakespeareDataset
from .dataset.sent140_dataset import Sent140Dataset
from .nlp_utils.dataset_vocab.sample_build_vocab import get_built_vocab


def get_LEAF_dataloader(dataset, client_id=0, batch_size=128):
    """Get dataloader with ``batch_size`` param for client with ``client_id``

    Args:
        dataset (str): dataloader for dataset
        client_id (int, optional): assigned client_id to get dataloader for this client. Defaults to 0
        batch_size (int, optional): the number of batch size for dataloader. Defaults to 128

    Returns:
        A tuple with train dataloader and test dataloader for the client with `client_id`

    Examples:
        trainloader, testloader = get_LEAF_dataloader(dataset='femnist', client_id=args.local_rank - 1)
    """

    if dataset == 'femnist':
        trainset = FemnistDataset(client_id=client_id, data_root='../data/femnist/data', is_train=True)
        testset = FemnistDataset(client_id=client_id, data_root='../data/femnist/data', is_train=False)
    elif dataset == 'shakespeare':
        trainset = ShakespeareDataset(client_id=client_id, data_root='../data/shakespeare/data', is_train=True)
        testset = ShakespeareDataset(client_id=client_id, data_root='../data/shakespeare/data', is_train=False)
    elif dataset == 'sent140':
        trainset = Sent140Dataset(client_id=client_id, data_root='../data/sent140/data', is_train=True)
        testset = Sent140Dataset(client_id=client_id, data_root='../data/sent140/data', is_train=False)
        vocab = get_built_vocab(dataset)
        # vocab = Vocab(trainset.data_token, vocab_limit_size=80000)
        trainset.token2seq(vocab, maxlen=300)
        testset.token2seq(vocab, maxlen=300)

    trainloader = torch.utils.data.DataLoader(
        trainset,
        batch_size=batch_size,
        drop_last=False)  # avoid train dataloader size 0
    testloader = torch.utils.data.DataLoader(
        testset,
        batch_size=len(testset),
        drop_last=False,
        shuffle=False)
    
    return trainloader, testloader
