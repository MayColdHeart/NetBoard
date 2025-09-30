using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace NetboardApi.Migrations
{
    /// <inheritdoc />
    public partial class UniqueProtocolName : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateIndex(
                name: "IX_Protocol_Name",
                table: "Protocol",
                column: "Name");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropIndex(
                name: "IX_Protocol_Name",
                table: "Protocol");
        }
    }
}
