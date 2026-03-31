public abstract class ReportHandler {

    protected ReportHandler next;

    public ReportHandler setNext(ReportHandler next) {
        this.next = next;
        return next;
    }

    public void handle(String report) {
        process(report);
        if (next != null) next.handle(report);
    }

    protected abstract void process(String report);
}

// Logging
public class LoggingHandler extends ReportHandler {
    protected void process(String report) {
        System.out.println("Report generated");
    }
}


// Email
public class EmailHandler extends ReportHandler {
    protected void process(String report) {
        System.out.println("Email sent");
    }
}


// Archive
public class ArchiveHandler extends ReportHandler {
    protected void process(String report) {
        System.out.println("Report archived");
    }
}