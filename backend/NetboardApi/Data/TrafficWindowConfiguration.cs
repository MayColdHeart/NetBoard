using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using NetboardApi.Models;

namespace NetboardApi.Data;

public class TrafficWindowConfig : IEntityTypeConfiguration<TrafficWindow>
{
    public void Configure(EntityTypeBuilder<TrafficWindow> builder)
    {
        builder.ToTable("TrafficWindow");

        builder.HasKey(tw => tw.Id);

        builder.Property(tw => tw.SourceIP)
            .IsRequired()
            .HasMaxLength(45);

        builder.Property(tw => tw.TotalSizeBytes)
            .IsRequired();

        builder.Property(tw => tw.ProtocolId)
            .IsRequired();

        builder.HasOne(tw => tw.Protocol)
            .WithMany()
            .OnDelete(DeleteBehavior.Restrict);
    }
}
