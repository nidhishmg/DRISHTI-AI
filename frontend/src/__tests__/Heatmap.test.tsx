import { render, screen } from "@testing-library/react";
import Heatmap from "../components/Heatmap";
import { Cluster } from "../types";

const mockClusters: Cluster[] = [
    {
        id: "1",
        title: "Test Cluster",
        summary: "Test Summary",
        trend_metrics: { count_30d: 10, growth_rate: 5 },
        geo_distribution: { "Test": 100 },
        confidence_score: 0.9,
    }
];

describe("Heatmap Component", () => {
    it("renders correctly with data", () => {
        const { container } = render(<Heatmap clusters={mockClusters} />);
        expect(container).toMatchSnapshot();
    });

    it("renders correctly without data", () => {
        const { container } = render(<Heatmap clusters={[]} />);
        expect(container).toMatchSnapshot();
    });
});
