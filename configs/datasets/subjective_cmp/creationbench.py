from opencompass.openicl.icl_prompt_template import PromptTemplate
from opencompass.openicl.icl_retriever import ZeroRetriever
from opencompass.openicl.icl_inferencer import GenInferencer
from opencompass.openicl.icl_evaluator import LMEvaluator
from opencompass.datasets import AlignmentBenchDataset
from mmengine.config import read_base

subjective_reader_cfg = dict(
    input_columns=['question', 'capability', 'prefix', 'suffix'],
    output_column='judge',
    )

subjective_all_sets = [
    "creation_v0.1",
]
data_path ="data/subjective/creationbench"

creationbench_config_path = "data/subjective/creationbench/"
creationbench_config_name = 'config/multi-dimension'

subjective_datasets = []

for _name in subjective_all_sets:
    subjective_infer_cfg = dict(
            prompt_template=dict(
                type=PromptTemplate,
                template=dict(round=[
                    dict(
                        role='HUMAN',
                        prompt="{question}"
                    ),
                ]),
            ),
            retriever=dict(type=ZeroRetriever),
            inferencer=dict(type=GenInferencer),
        )

    subjective_eval_cfg = dict(
        evaluator=dict(
            type=LMEvaluator,
            prompt_template=dict(
                type=PromptTemplate,
                template=dict(round=[
                    dict(
                        role='HUMAN',
                        prompt = "{prefix}[助手的答案开始]\n{prediction}\n[助手的答案结束]\n"
                    ),
                ]),
            ),
        ),
        pred_role="BOT",
    )

    subjective_datasets.append(
        dict(
            abbr=f"{_name}",
            type=CreationBenchDataset,
            path=data_path,
            name=_name,
            creationbench_config_path=creationbench_config_path,
            creationbench_config_name=creationbench_config_name,
            reader_cfg=subjective_reader_cfg,
            infer_cfg=subjective_infer_cfg,
            eval_cfg=subjective_eval_cfg
        ))