// Sales report
public class SalesReport extends AbstractReportGenerator {

    private ReportHandler handler;

    public SalesReport(ReportHandler handler) {
        this.handler = handler;
    }

    protected void appendHeader(StringBuilder sb) {
        sb.append("=== SALES REPORT ===");
    }

    protected Object getData(Date from, Date to) {
        return new ArrayList<>(); 
    }

    protected void processData(StringBuilder sb, Object data) {
        var list = (List<Sale>) data;
        double total = 0;
        for (Sale s : list) {
            sb.append(s.getId() + ": " + s.getAmount());
            total += s.getAmount();
        }
        sb.append("Total: " + total);
    }

    protected void postProcess(String report) {
        handler.handle(report);
    }
}


// Inventory report
public class InventoryReport extends AbstractReportGenerator {

    private ReportHandler handler;

    public InventoryReport(ReportHandler handler) {
        this.handler = handler;
    }

    protected void appendHeader(StringBuilder sb) {
        sb.append("=== INVENTORY REPORT ===");
    }

    protected Object getData(Date from, Date to) {
        return new ArrayList<>();
    }

    protected void processData(StringBuilder sb, Object data) {
        var list = (List<Item>) data;
        for (Item i : list) {
            sb.append(i.getName() + ": " + i.getStock());
        }
    }

    protected void appendFooter(StringBuilder sb) {
        sb.append("Generated at: " + new Date());
    }

    protected void postProcess(String report) {
        handler.handle(report);
    }
}


// Financial report
public class FinancialReport extends AbstractReportGenerator {

    private ReportHandler handler;

    public FinancialReport(ReportHandler handler) {
        this.handler = handler;
    }

    protected void appendHeader(StringBuilder sb) {
        sb.append("=== FINANCIAL REPORT ===");
    }

    protected Object getData(Date from, Date to) {
        return new ArrayList<>();
    }

    protected void processData(StringBuilder sb, Object data) {
        sb.append("Financial data...");
    }

    protected void postProcess(String report) {
        handler.handle(report);
    }
}