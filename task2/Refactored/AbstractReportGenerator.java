public abstract class AbstractReportGenerator {

    public final String generate(Date from, Date to) {
        StringBuilder sb = new StringBuilder();

        appendHeader(sb);
        appendPeriod(sb, from, to);

        var data = getData(from, to);

        if (isEmpty(data)) {
            sb.append("No data");
            return sb.toString();
        }

        processData(sb, data);

        appendFooter(sb);

        String result = sb.toString();

        postProcess(result);

        return result;
    }

    protected abstract void appendHeader(StringBuilder sb);
    protected abstract Object getData(Date from, Date to);
    protected abstract void processData(StringBuilder sb, Object data);

    protected void appendPeriod(StringBuilder sb, Date from, Date to) {
        sb.append("Period: " + from + " - " + to);
    }

    protected void appendFooter(StringBuilder sb) {}

    protected boolean isEmpty(Object data) {
        return ((java.util.List<?>)data).isEmpty();
    }

    protected abstract void postProcess(String report);
}