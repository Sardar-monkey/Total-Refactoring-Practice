// Интерфейс которому должны следовать наследуемые классы
// То есть все должны иметь метод format()
public interface ReportFormatter {
    String format(String content);
}

// text
public class TextFormatter implements ReportFormatter {
    public String format(String content) {
        return content;
    }
}

// CSV
public class CsvFormatter implements ReportFormatter {
    public String format(String content) {
        return content.replace(":", ",");
    }
}

// HTML
public class HtmlFormatter implements ReportFormatter {
    public String format(String content) {
        return "<html><body><pre>" + content + "</pre></body></html>";
    }
}