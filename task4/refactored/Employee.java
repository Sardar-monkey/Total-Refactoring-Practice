public class Employee {
    private String name;
    private String department;
    private SalaryCalculation salaryCalculation;
    private BankDetails bankDetails;
    private Address address;

    public Employee(String name, String department,
                    SalaryCalculation salaryCalculation,
                    BankDetails bankDetails,
                    Address address) {
        this.name = name;
        this.department = department;
        this.salaryCalculation = salaryCalculation;
        this.bankDetails = bankDetails;
        this.address = address;
    }

    public void sendPayslip() {
        double net = salaryCalculation.calculateNetSalary();
        PostalService.send(address.getFullAddress(), "Payslip: " + net);
        BankService.transfer(bankDetails.getPaymentDetails(), net);
        Logger.log(name + " paid " + net + " to " + bankDetails.getPaymentDetails());
    }
}