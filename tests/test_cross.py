import tntorch as tn
import torch
from util import random_format


def test_domain():

    def function(Xs):
        return 1. / torch.sum(Xs, dim=1)

    domain = [torch.linspace(1, 10, 10) for n in range(3)]
    t = tn.cross(function=function, domain=domain, ranks_tt=3, function_arg='matrix')
    gt = torch.meshgrid(domain)
    gt = 1. / sum(gt)

    assert tn.relative_error(gt, t) < 5e-2


def test_tensors():

    for i in range(100):
        t = random_format([10] * 6)
        t2 = tn.cross(function=lambda x: x, tensors=t, ranks_tt=15, verbose=False)
        assert tn.relative_error(t, t2) < 1e-6


def test_ops():

    x, y, z, w = tn.meshgrid([32]*4)
    t = x + y + z + w + 1
    assert tn.relative_error(1/t.torch(), 1/t) < 1e-4
    assert tn.relative_error(torch.cos(t.torch()), tn.cos(t)) < 1e-4
    assert tn.relative_error(torch.exp(t.torch()), tn.exp(t)) < 1e-4
