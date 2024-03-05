"""
Schedule running OCR Add-On on a project of documents on a schedule.
"""
from itertools import islice
from documentcloud.addon import AddOn


class Scheduler(AddOn):
    """An example Add-On for DocumentCloud."""

    def main(self):
        """ Runs the selected OCR engine on a batch of documents """
        batch_size = self.data.get("batch_size")
        project_id = self.data.get("project_id")
        ocr_engine = self.data.get("ocr_engine")
        batch_num = 1

        if ocr_engine == "azure":
            run_id = 544
        if ocr_engine == "google":
            run_id = 542
        if ocr_engine == "doctr":
            run_id = 549

        documents = self.client.documents.search(
            f"+project:{project_id} -data_ocr_engine:*"
        )

        for i in range(batch_num):
            # Pull out the IDs for a batch of the documents
            doc_ids = [
                d.id for d in islice(documents, i * batch_size, (i + 1) * batch_size)
            ]

            self.client.post(
                "addon_runs/",
                json={
                    "addon": run_id,
                    "parameters": {
                        "to_tag": True
                    },
                    "documents": doc_ids,
                    "dismissed": True,
                },
            )

if __name__ == "__main__":
    Scheduler().main()
