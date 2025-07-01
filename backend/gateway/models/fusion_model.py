class FusionModel:
    @staticmethod
    def get_RRF_sorted(k, ids_1, ids_2):
        final_scores = {}
        for i, id_1 in enumerate(ids_1):
            if id_1 not in final_scores:
                final_scores[id_1] = k
            final_scores[id_1] += 1 / (i + 1)

        for i, id_2 in enumerate(ids_2):
            if id_2 not in final_scores:
                final_scores[id_2] = k
            final_scores[id_2] += 1 / (i + 1)

        sorted_results = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        return [id for id, score in sorted_results]