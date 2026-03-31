public class SalaryCalculation {
    private final double baseSalary;
    private final int hoursWorked;
    private final int overtimeHours;
    private final double taxRate;
    private final double pensionRate;
    private final double healthInsuranceRate;

    public SalaryCalculation(double baseSalary, int hoursWorked, int overtimeHours,
                             double taxRate, double pensionRate, double healthInsuranceRate) {
        this.baseSalary = baseSalary;
        this.hoursWorked = hoursWorked;
        this.overtimeHours = overtimeHours;
        this.taxRate = taxRate;
        this.pensionRate = pensionRate;
        this.healthInsuranceRate = healthInsuranceRate;
    }

    public double calculateNetSalary() {
        double gross = baseSalary + (overtimeHours * baseSalary / 160 * 1.5);
        double tax = gross * taxRate;
        double pension = gross * pensionRate;
        double health = gross * healthInsuranceRate;
        return gross - tax - pension - health;
    }
}