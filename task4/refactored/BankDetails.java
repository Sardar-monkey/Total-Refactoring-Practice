import java.util.Objects;

public final class BankDetails {
    private final String bankName;
    private final String bankAccount;
    private final String bankRoutingNumber;

    public BankDetails(String bankName, String bankAccount, String bankRoutingNumber) {
        this.bankName = bankName;
        this.bankAccount = bankAccount;
        this.bankRoutingNumber = bankRoutingNumber;
    }

    public String getPaymentDetails() {
        return bankName + " " + bankAccount + " (" + bankRoutingNumber + ")";
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof BankDetails)) return false;
        BankDetails that = (BankDetails) o;
        return Objects.equals(bankName, that.bankName) &&
               Objects.equals(bankAccount, that.bankAccount) &&
               Objects.equals(bankRoutingNumber, that.bankRoutingNumber);
    }

    @Override
    public int hashCode() {
        return Objects.hash(bankName, bankAccount, bankRoutingNumber);
    }
}